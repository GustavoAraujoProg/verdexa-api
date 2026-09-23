from io import BytesIO
from uuid import uuid4
import warnings
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import HTTPException, UploadFile
from config import settings

Image.MAX_IMAGE_PIXELS = 20_000_000


def salvar_imagem(arquivo: UploadFile):
    limite = settings.max_upload_mb * 1024 * 1024
    dados = arquivo.file.read(limite + 1)
    if len(dados) > limite:
        raise HTTPException(413, 'Imagem excede o limite de tamanho')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(BytesIO(dados)) as imagem:
                if imagem.format not in {'JPEG', 'PNG', 'WEBP'}:
                    raise HTTPException(415, 'Use JPEG, PNG ou WEBP')
                imagem.load()
                limpa = ImageOps.exif_transpose(imagem).convert('RGB')
                limpa.thumbnail((2048, 2048))
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise HTTPException(422, 'Arquivo inválido ou imagem com dimensões excessivas')
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    caminho = settings.upload_dir / f'{uuid4().hex}.jpg'
    try:
        limpa.save(caminho, 'JPEG', quality=90)
    except Exception:
        caminho.unlink(missing_ok=True)
        raise
    return caminho
