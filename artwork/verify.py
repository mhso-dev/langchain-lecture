"""Verify all authored frames, published assets, and notebook attachments."""
import base64
import io
import html
import json
from collections import Counter
from PIL import Image, ImageChops, ImageStat
from render import COLS, FRAMES, ROOT, SCENES, TINTS
from studio import Board, H, W

def verify(scene):
    name = f'chapter{scene.chapter:02}'
    folder = ROOT/'site'/name
    markup = (folder/'index.html').read_text()
    assert markup.count(f'id="motion-{scene.key}"') == 1, scene.key
    assert html.escape(scene.title) in markup and html.escape(scene.explanation) in markup, scene.key
    notebook = json.loads((folder/(name+'.ipynb')).read_bytes())
    asset = scene.key + '.gif'
    cells = [c for c in notebook['cells'] if asset in c.get('attachments', {})]
    assert len(cells) == 1 and f'attachment:{asset}' in ''.join(cells[0]['source']), scene.key
    assert scene.explanation in ''.join(cells[0]['source']), scene.key
    binary = base64.b64decode(cells[0]['attachments'][asset]['image/gif'],validate=True)
    with (Image.open(io.BytesIO(binary))) as gif, Image.open(folder/'motion'/(scene.key+'.webp')) as sheet, Image.open(folder/'motion'/(scene.key+'-still.webp')) as still:
        assert gif.n_frames > 1, scene.key
        w, h = still.size
        for index in range(FRAMES):
            board = Board(TINTS[(scene.chapter-1) % len(TINTS)])
            scene.draw(board, index/(FRAMES-1))
            x, y = index % COLS * w, index // COLS * h
            frame = sheet.crop((x, y, x+w, y+h)).convert('RGB')
            assert not ImageChops.difference(frame,board.image).getbbox(), (scene.key,index)
            if index == FRAMES-1:
                assert not ImageChops.difference(frame,still.convert('RGB')).getbbox(),scene.key
            if index in (0, FRAMES-1):
                gif.seek(0 if index == 0 else gif.n_frames-1)
                diff = ImageChops.difference(frame.resize((W,H),Image.Resampling.LANCZOS),gif.convert('RGB'))
                assert max(ImageStat.Stat(diff).mean) < 3, (scene.key,index)
    return scene.chapter

if __name__ == '__main__':
    counts = Counter(verify(scene) for scene in SCENES.values())
    assert set(counts) == set(range(1,117))
    print(f'{len(counts)} chapters, {sum(counts.values())} animations and notebook GIFs, {FRAMES*sum(counts.values())} frames verified.')
