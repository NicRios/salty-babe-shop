// Rasterize the outlined vectors with transparency intact (requires sharp).
const path = require('node:path');
const sharp = require('sharp');
(async () => {
  for (const name of ['black', 'white']) {
    const destination = path.join(__dirname, `salty-babe-${name}.png`);
    await sharp(path.join(__dirname, `salty-babe-${name}.svg`), { density: 300 })
      .resize({ width: 3600 }).png().toFile(destination);
    const { data, info } = await sharp(destination).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    let transparent = 0, opaque = 0;
    for (let i = 0; i < data.length; i += 4) {
      if (data[i + 3] === 0) transparent++;
      if (data[i + 3] === 255) opaque++;
      if (data[i + 3] > 0 && data[i] !== (name === 'black' ? 0 : 255)) throw new Error('Unexpected logo color');
    }
    if (!transparent || !opaque) throw new Error('Missing transparency or lettering');
    for (let x = 0; x < info.width; x++) {
      if (data[x*4+3] || data[((info.height-1)*info.width+x)*4+3]) throw new Error('Opaque image border');
    }
    console.log(`${name}: ${info.width} x ${info.height}, RGBA, ${(transparent/(info.width*info.height)*100).toFixed(1)}% fully transparent`);
  }
})();
