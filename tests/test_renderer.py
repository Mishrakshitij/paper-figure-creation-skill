"""Behavioral tests for evidence gating, publication exports, and layout warnings."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/paper-figure-creation/scripts'))
from render_figure import geometry_check,render


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out=Path(self.tmp.name)/'figure'
        assets=ROOT/'skills/paper-figure-creation/assets'
        self.teaser=json.loads((assets/'teaser-template.json').read_text())
        self.method=json.loads((assets/'method-template.json').read_text())

    def test_false_gain_never_reaches_export(self):
        self.teaser['evidence']['claims'][0]['display_value']=50
        with self.assertRaisesRegex(ValueError,'Evidence validation failed'):
            render(self.teaser,self.out,formats=('svg',))
        self.assertFalse(self.out.with_suffix('.svg').exists())

    def test_exact_physical_export_and_editable_svg(self):
        report=render(self.teaser,self.out,formats=('svg','png'))
        self.assertEqual(report['warnings'],[])
        with Image.open(self.out.with_suffix('.png')) as im:
            self.assertEqual(im.size,(2160,1020))
            self.assertAlmostEqual(im.info['dpi'][0],300,delta=.1)
        tree=ET.parse(self.out.with_suffix('.svg'))
        self.assertGreater(len(tree.findall('.//{http://www.w3.org/2000/svg}text')),15)

    def test_native_diagram_retains_nodes_and_routes(self):
        report=render(self.method,self.out,formats=('svg',))
        self.assertEqual(report['warnings'],[])
        cells=ET.parse(self.out.with_suffix('.drawio')).findall('.//mxCell')
        ids={c.attrib['id'] for c in cells}
        self.assertTrue({n['id'] for n in self.method['nodes']} <= ids)
        self.assertEqual(sum(c.attrib.get('edge')=='1' for c in cells),len(self.method['edges']))
        self.assertTrue(any(c.find('./mxGeometry/Array/mxPoint') is not None for c in cells))

    def test_node_overlap_and_unknown_endpoint_are_rejected(self):
        self.method['nodes'][1].update(x=.005,y=.37)
        self.assertTrue(any('Overlapping' in e for e in geometry_check(self.method)[0]))
        self.method['edges'][0]['target']='absent'
        self.assertTrue(any('Unknown edge' in e for e in geometry_check(self.method)[0]))

    def test_edges_through_unrelated_nodes_warn(self):
        self.method['nodes'].append({'id':'obstacle','x':.54,'y':.69,'w':.05,'h':.08,'label':'X'})
        self.assertTrue(any('crosses node obstacle' in w for w in geometry_check(self.method)[1]))

    def test_node_overflow_and_offpage_title_are_reported(self):
        self.method['nodes'][1]['label']='This label is deliberately much too long for its box'
        self.method['figure']['title']='A long title ' * 18
        report=render(self.method,self.out,formats=('svg',))
        self.assertTrue(any('overflow node frozen' in w for w in report['warnings']))
        self.assertTrue(any('Text leaves the page' in w for w in report['warnings']))

    def test_unrendered_ticks_outside_limits_do_not_warn(self):
        self.teaser['charts'][0]['xlim']=[72,84]
        self.teaser['charts'][0]['xticks']=[-1000,75,80,1000]
        report=render(self.teaser,self.out,formats=('svg',))
        self.assertFalse(any("'-1000'" in w or "'1000'" in w for w in report['warnings']))

    def test_bar_truncation_is_blocked(self):
        self.teaser['charts'][1]['xlim']=[60,130]
        with self.assertRaises(ValueError):
            render(self.teaser,self.out,formats=('svg',))


    def test_chart_limits_cannot_hide_declared_points(self):
        self.teaser['charts'][0]['xlim']=[80,82]
        with self.assertRaisesRegex(ValueError,'Data point outside x limits'):
            render(self.teaser,self.out,formats=('svg',))
        self.assertFalse(self.out.with_suffix('.svg').exists())

    def test_nonpositive_scatter_log_coordinate_is_rejected(self):
        chart=self.teaser['charts'][0]
        chart.update(type='scatter',xscale='log',x_values=[0,1,2],
                     x_source_id='demo',x_source_location='Illustrative schedule')
        chart.pop('xlim');chart.pop('xticks')
        with self.assertRaisesRegex(ValueError,'Nonpositive log x coordinate'):
            render(self.teaser,self.out,formats=('svg',))

    def test_custom_concept_geometry_is_checked(self):
        self.teaser['concept']={**copy.deepcopy(self.method),'kind':'custom'}
        self.teaser['concept']['nodes'][1].update(x=.005,y=.37)
        with self.assertRaisesRegex(ValueError,'Concept: Overlapping nodes'):
            render(self.teaser,self.out,formats=('svg',))
        self.teaser['concept']['edges'][0]['target']='absent'
        self.assertTrue(any('Concept: Unknown edge' in e for e in geometry_check(self.teaser)[0]))

    def test_custom_concept_edges_and_text_are_checked(self):
        self.teaser['concept']={'kind':'custom','title':'Concept','nodes':[
            {'id':'long','x':.05,'y':.35,'w':.20,'h':.2,
             'label':'A deliberately overflowing concept label'},
            {'id':'target','x':.75,'y':.35,'w':.20,'h':.2,'label':'B'},
            {'id':'obstacle','x':.45,'y':.35,'w':.10,'h':.2,'label':'C'}],
            'edges':[{'source':'long','target':'target'}]}
        report=render(self.teaser,self.out,formats=('svg',))
        self.assertTrue(any('Concept: Edge long -> target crosses node obstacle' in w for w in report['warnings']))
        self.assertTrue(any('Concept: Text may overflow node long' in w for w in report['warnings']))

    def test_drawio_preserves_headless_edges(self):
        self.method['edges'][0]['arrow']=False
        render(self.method,self.out,formats=('svg',))
        cells=ET.parse(self.out.with_suffix('.drawio')).findall('.//mxCell')
        first=next(c for c in cells if c.attrib['id']=='edge-0')
        second=next(c for c in cells if c.attrib['id']=='edge-1')
        self.assertIn('endArrow=none;',first.attrib['style'])
        self.assertIn('endArrow=block;',second.attrib['style'])

    def test_drawio_mask_hides_original_token_and_selected_state(self):
        self.method['nodes'][0]['representation'].update(
            labels=['secret','b','c','d','e','f','g','h'],selected=[0,1],mask=[0])
        render(self.method,self.out,formats=('svg',))
        cells=ET.parse(self.out.with_suffix('.drawio')).findall('.//mxCell')
        tile=next(c for c in cells if c.attrib['id']=='input-tile-0')
        unmasked=next(c for c in cells if c.attrib['id']=='input-tile-1')
        self.assertEqual(tile.attrib['value'],'·')
        self.assertIn('fillColor=#FFFFFF;',tile.attrib['style'])
        self.assertIn('strokeColor=#DCE2E5;',tile.attrib['style'])
        self.assertEqual(unmasked.attrib['value'],'b')
        self.assertIn('fillColor=#E6F2F3;',unmasked.attrib['style'])
        self.assertFalse(any(c.attrib.get('value')=='secret' for c in cells))


if __name__=='__main__':
    unittest.main()
