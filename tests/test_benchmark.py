"""Benchmark eligibility, protocol omissions, and reusable drawing checks."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/paper-figure-creation/scripts'))
from render_figure import geometry_check, render
from validate_evidence import validate_spec


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads((ROOT / 'skills/paper-figure-creation/assets/benchmark-template.json').read_text())
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'figure'

    def codes(self, spec=None):
        return {error['code'] for error in validate_spec(spec or self.spec)['errors']}

    def test_setup_without_performance_results_is_valid(self):
        report = validate_spec(self.spec)
        self.assertTrue(report['valid'], report['errors'])
        self.assertEqual(report['computed_claims'], [])
        self.assertTrue(any(w['code'] == 'synthetic_not_evidence' for w in report['warnings']))

    def test_absent_or_unresolved_setup_never_reaches_export(self):
        for presence in ('absent', 'unclear', None):
            with self.subTest(presence=presence):
                self.spec['benchmark_setup']['presence'] = presence
                with self.assertRaisesRegex(ValueError, 'verified setup'):
                    render(self.spec, self.out, formats=('svg',))
                self.assertFalse(self.out.with_suffix('.svg').exists())

    def test_contract_and_specific_source_anchor_are_required(self):
        missing = copy.deepcopy(self.spec)
        missing.pop('benchmark_setup')
        self.assertIn('benchmark_setup', self.codes(missing))
        for field, value in (('source_id', 'not-declared'), ('source_location', ' ')):
            with self.subTest(field=field):
                spec = copy.deepcopy(self.spec)
                spec['benchmark_setup'][field] = value
                self.assertIn('benchmark_source', self.codes(spec))

    def test_unit_construction_and_scoring_cannot_be_omitted(self):
        for field in ('unit_of_evaluation', 'instance_construction', 'evaluation'):
            with self.subTest(field=field):
                spec = copy.deepcopy(self.spec)
                spec['benchmark_setup'].pop(field)
                self.assertIn('benchmark_contract', self.codes(spec))

    def test_static_benchmark_does_not_require_an_agent_loop(self):
        setup = self.spec['benchmark_setup']
        setup.update(family='static_benchmark', contribution='new_benchmark',
                     unit_of_evaluation='One annotated image question',
                     instance_construction='Hand-authored illustrative question set',
                     agent_visible=['Image', 'Question'], evaluator_only=['Reference answer'],
                     evaluation='Match the response against the illustrative reference')
        for field in ('observation', 'actions', 'state_transition', 'reset', 'termination'):
            setup.pop(field)
        # Only checking the contract here, not claiming the interaction scaffold
        # above becomes a faithful static-benchmark drawing by changing metadata.
        self.assertTrue(validate_spec(self.spec)['valid'])

    def test_interactive_and_mixed_setup_require_episode_contract(self):
        for family in ('interactive_environment', 'mixed'):
            for field in ('observation', 'actions', 'state_transition', 'reset', 'termination'):
                with self.subTest(family=family, field=field):
                    spec = copy.deepcopy(self.spec)
                    spec['benchmark_setup']['family'] = family
                    spec['benchmark_setup'].pop(field)
                    self.assertIn('benchmark_episode', self.codes(spec))

    def test_visibility_must_be_explicit_but_empty_category_is_allowed(self):
        self.spec['benchmark_setup']['evaluator_only'] = []
        self.assertTrue(validate_spec(self.spec)['valid'])
        self.spec['benchmark_setup'].pop('agent_visible')
        self.assertIn('benchmark_visibility', self.codes())
        self.spec['nodes'][0]['visibility'] = 'guess'
        self.assertIn('benchmark_node_visibility', self.codes())

    def test_synthetic_benchmark_cannot_become_final(self):
        self.spec['status'] = 'final'
        with self.assertRaisesRegex(ValueError, 'labeled drafts only'):
            render(self.spec, self.out, formats=('svg',))
        self.assertFalse(self.out.with_suffix('.svg').exists())

    def test_benchmark_exports_editable_text_routes_and_separate_judge(self):
        report = render(self.spec, self.out, formats=('svg', 'png'))
        self.assertEqual(report['figure_kind'], 'benchmark')
        self.assertEqual(report['warnings'], [])
        with Image.open(self.out.with_suffix('.png')) as image:
            self.assertEqual(image.size, (2160, 1350))
        svg = ET.parse(self.out.with_suffix('.svg'))
        visible = ' '.join(svg.getroot().itertext())
        self.assertIn('EVALUATOR ONLY', visible)
        self.assertIn('ILLUSTRATIVE SETUP', visible)
        doc = ET.parse(self.out.with_suffix('.drawio'))
        self.assertEqual(doc.find('./diagram').attrib['name'], 'Benchmark / environment')
        cells = doc.findall('.//mxCell')
        self.assertTrue({n['id'] for n in self.spec['nodes']} <= {c.attrib['id'] for c in cells})
        self.assertEqual(sum(c.attrib.get('edge') == '1' for c in cells), len(self.spec['edges']))
        self.assertTrue(any(c.find('./mxGeometry/Array/mxPoint') is not None for c in cells))
        # The hidden checker has no outgoing path into the agent in this fixture.
        self.assertFalse(any(c.attrib.get('source') == 'evaluator' and
                             c.attrib.get('target') == 'agent' for c in cells))

    def test_benchmark_collision_and_unknown_endpoint_checks_are_retained(self):
        self.spec['nodes'][1].update(x=.02, y=.61)
        self.spec['edges'][0]['target'] = 'absent'
        errors, _ = geometry_check(self.spec)
        self.assertTrue(any('Overlapping nodes' in e for e in errors))
        self.assertTrue(any('Unknown edge endpoint' in e for e in errors))
        with self.assertRaises(ValueError):
            render(self.spec, self.out, formats=('svg',))

    def test_benchmark_text_overflow_is_reported(self):
        self.spec['nodes'][1]['label'] = 'This benchmark agent label is deliberately too wide'
        report = render(self.spec, self.out, formats=('svg',))
        self.assertTrue(any('Text may overflow node agent' in w for w in report['warnings']))

    def test_benchmark_edges_crossing_unrelated_nodes_are_reported(self):
        self.spec['nodes'].append({'id': 'obstacle', 'x': .65, 'y': .63,
                                   'w': .035, 'h': .07, 'label': 'X'})
        _, warnings = geometry_check(self.spec)
        self.assertTrue(any('crosses node obstacle' in w for w in warnings))


if __name__ == '__main__':
    unittest.main()
