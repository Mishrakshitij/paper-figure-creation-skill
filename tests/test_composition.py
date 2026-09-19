"""Tests for physical SVG composition and safe, editable vector imports."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/paper-figure-creation/scripts'))
from compose_svg import compose, sanitize_svg

SVG = '{http://www.w3.org/2000/svg}'


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root / 'output' / 'figure'
        self.spec = {
            'canvas': {'width_pt': 360, 'height_pt': 180},
            'assets': [],
            'overlays': [{'type': 'text', 'x': 10, 'y': 15, 'text': 'Editable label', 'font_size_pt': 8}],
        }

    def vector(self, name='plot', svg=None, box=None):
        svg = svg or '''<svg xmlns="http://www.w3.org/2000/svg" width="180pt" height="100pt" viewBox="0 0 180 100">
        <defs><clipPath id="clip"><rect width="160" height="90"/></clipPath></defs>
        <style>* {stroke-linecap: butt} .label {font-size: 8px; fill: #173544}</style>
        <g clip-path="url(#clip)"><path d="M 0 0 L 100 80" stroke="black"/><text class="label" x="10" y="30">Observed</text></g>
        </svg>'''
        (self.root / f'{name}.svg').write_text(svg)
        self.spec['assets'].append({'id': name, 'kind': 'vector', 'path': f'{name}.svg', 'box_pt': box or [0, 30, 180, 100], 'provenance': {'source': 'test fixture', 'role': 'constructed example'}})

    def test_vector_ids_refs_css_and_live_text_survive_two_imports(self):
        self.vector('left')
        self.vector('right', box=[180, 30, 180, 100])
        report = compose(self.spec, self.root, self.out, ('svg',))
        root = ET.parse(self.out.with_suffix('.svg')).getroot()
        ids = [item.get('id') for item in root.iter() if item.get('id')]
        self.assertEqual(len(ids), len(set(ids)))
        clips = [item.get('clip-path') for item in root.iter() if item.get('clip-path')]
        self.assertIn('url(#import-0-clip)', clips)
        self.assertIn('url(#import-1-clip)', clips)
        labels = root.findall(f'.//{SVG}text')
        self.assertEqual(len(labels), 3)
        self.assertTrue(any('font-size:8px' in item.get('style', '') for item in labels))
        self.assertEqual(root.findall(f'.//{SVG}style'), [])
        self.assertEqual(report['minimum_font_size_pt'], 8)

    def test_transformed_imported_labels_are_measured_in_final_points(self):
        self.vector(svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><g transform="translate(8 4) scale(0.5)"><text style="font: 400 16px sans-serif" x="0" y="16">Scaled</text></g></svg>''', box=[0, 30, 100, 50])
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertEqual(report['assets'][0]['minimum_font_size_pt'], 4)
        self.assertTrue(any('4 pt' in warning for warning in report['warnings']))
        self.assertEqual(report['canvas_pt'], [360, 180])

    def test_overlay_font_size_is_physical_not_pixel_canvas_dependent(self):
        self.spec['canvas'] = {'width_pt': 89 / 25.4 * 72, 'height_pt': 100}
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertEqual(report['minimum_font_size_pt'], 8)
        root = ET.parse(self.out.with_suffix('.svg')).getroot()
        self.assertTrue(root.get('width').endswith('pt'))
        self.assertEqual(root.find(f'.//{SVG}text').get('font-size'), '8.0')

    def test_raster_embedded_with_actual_ppi_and_hash(self):
        Image.new('RGB', (600, 300), 'white').save(self.root / 'asset.png')
        self.spec['assets'] = [{'id': 'illustration', 'kind': 'raster', 'path': 'asset.png', 'box_pt': [0, 25, 144, 72], 'provenance': {'source': 'generated fixture', 'role': 'illustration'}}]
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertEqual(report['assets'][0]['effective_ppi'], 300)
        self.assertEqual(len(report['assets'][0]['sha256']), 64)
        image = ET.parse(self.out.with_suffix('.svg')).find(f'.//{SVG}image')
        self.assertTrue(image.get('{http://www.w3.org/1999/xlink}href').startswith('data:image/png;base64,'))

    def test_active_external_and_unresolved_resources_rejected(self):
        snippets = [
            '<script>alert(1)</script>',
            '<rect onclick="alert(1)"/>',
            '<image href="https://example.com/asset.png"/>',
            '<rect fill="url(https://example.com/fill.svg)"/>',
            '<style>rect {fill: url(https://example.com/a)}</style>',
            '<use href="#missing"/>',
            '<foreignObject/>',
        ]
        for snippet in snippets:
            with self.subTest(snippet=snippet), self.assertRaises(ValueError):
                sanitize_svg(f'<svg xmlns="http://www.w3.org/2000/svg">{snippet}</svg>'.encode(), 'prefix-')

    def test_asset_path_cannot_escape_or_hide_unsupported_styles(self):
        self.vector()
        self.spec['assets'][0]['path'] = '../escape.svg'
        with self.assertRaisesRegex(ValueError, 'inside'):
            compose(self.spec, self.root, self.out, ('svg',))
        self.assertFalse(self.out.with_suffix('.svg').exists())
        with self.assertRaisesRegex(ValueError, 'selector'):
            sanitize_svg(b'<svg xmlns="http://www.w3.org/2000/svg"><style>g > text {font-size:8px}</style></svg>', 'a-')

    def test_crop_requires_explicit_acknowledgment(self):
        self.vector()
        self.spec['assets'][0]['fit'] = 'cover'
        with self.assertRaisesRegex(ValueError, 'allow_crop'):
            compose(self.spec, self.root, self.out, ('svg',))
        self.spec['assets'][0]['allow_crop'] = True
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertTrue(report['assets'][0]['cropped'])

    def test_real_matplotlib_plot_imports_without_flattening(self):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        with matplotlib.rc_context({'svg.fonttype': 'none', 'font.size': 8}):
            fig, ax = plt.subplots(figsize=(2.5, 1.5))
            ax.plot([1, 2, 3], [2, 3, 2], marker='o', label='Observed')
            ax.set_xlabel('Budget'); ax.set_ylabel('Score'); ax.legend()
            fig.savefig(self.root / 'matplotlib.svg')
            plt.close(fig)
        self.spec['assets'] = [{'id': 'plot', 'kind': 'vector', 'path': 'matplotlib.svg', 'box_pt': [0, 30, 180, 108], 'provenance': {'source': 'constructed test fixture'}}]
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertGreater(report['assets'][0]['editable_text_count'], 5)
        self.assertAlmostEqual(report['assets'][0]['minimum_font_size_pt'], 8)
        root = ET.parse(self.out.with_suffix('.svg')).getroot()
        self.assertGreater(len(root.findall(f'.//{SVG}use')), 0)
        self.assertEqual(root.findall(f'.//{SVG}image'), [])

    def test_embedded_raster_resolution_is_audited_after_vector_placement(self):
        import base64
        import io
        data = io.BytesIO()
        Image.new('RGB', (100, 50), 'white').save(data, format='PNG')
        href = 'data:image/png;base64,' + base64.b64encode(data.getvalue()).decode()
        self.vector(svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><image width="200" height="100" href="{href}"/></svg>', box=[0, 30, 144, 72])
        report = compose(self.spec, self.root, self.out, ('svg',))
        self.assertEqual(report['assets'][0]['embedded_rasters'][0]['effective_ppi'], 50)
        self.assertTrue(any('Embedded raster' in warning for warning in report['warnings']))

    @unittest.skipUnless(shutil.which('inkscape'), 'Inkscape is needed for actual publication exports')
    def test_pdf_and_png_match_physical_canvas(self):
        from pypdf import PdfReader
        self.vector()
        report = compose(self.spec, self.root, self.out, ('svg', 'pdf', 'png'), dpi=144)
        with Image.open(self.out.with_suffix('.png')) as bitmap:
            self.assertEqual(bitmap.size, (720, 360))
        page = PdfReader(self.out.with_suffix('.pdf')).pages[0]
        self.assertAlmostEqual(float(page.mediabox.width), 360, places=2)
        self.assertAlmostEqual(float(page.mediabox.height), 180, places=2)
        self.assertTrue(all(item['verified'] for item in report['exports']))
        self.assertEqual(json.loads(self.out.with_suffix('.composition-report.json').read_text())['minimum_font_size_pt'], 8)


if __name__ == '__main__':
    unittest.main()
