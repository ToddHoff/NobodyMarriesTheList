// Build a Word file laid out for Vellum import from the chapter markdown files.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, AlignmentType } = require('docx');

const srcDir = process.argv[2];
const outFile = process.argv[3];

function smart(t) {
  t = t.replace(/(\d)'(\d)/g, '$1′$2');                 // 5'8 -> prime
  t = t.replace(/(^|[\s(“‘])'(?=\w)/g, '$1‘'); // opening single
  t = t.replace(/'/g, '’');                              // apostrophes, closing single
  t = t.replace(/(^|[\s(])"(?=\S)/g, '$1“');             // opening double
  t = t.replace(/"/g, '”');                              // closing double
  return t;
}

function runsFromInline(text, extra) {
  // *italic*, **bold** and ~~strike~~ spans
  const runs = [];
  let it = false, bd = false, st = false, buf = '';
  const flush = () => {
    if (buf === '') return;
    runs.push(new TextRun(Object.assign({ text: smart(buf), italics: it, bold: bd, strike: st }, extra || {})));
    buf = '';
  };
  for (let k = 0; k < text.length; ) {
    if (text.startsWith('**', k)) { flush(); bd = !bd; k += 2; continue; }
    if (text.startsWith('~~', k)) { flush(); st = !st; k += 2; continue; }
    if (text[k] === '*') { flush(); it = !it; k += 1; continue; }
    buf += text[k]; k += 1;
  }
  flush();
  if (it || bd || st) throw new Error('unbalanced marks in: ' + text.slice(0, 60));
  return runs;
}

const all = fs.readdirSync(srcDir);
const files = all.filter(f => /^(chapter-\d\d-(jo|cal)|epilogue-jo)\.md$/.test(f)).sort()
  .concat(all.filter(f => /^back-\d\d-[a-z-]+\.md$/.test(f)).sort());
const children = [];
const stats = { chapters: 0, back: 0, paragraphs: 0, notes: 0, screens: 0, breaks: 0, words: 0 };

for (const f of files) {
  const lines = fs.readFileSync(path.join(srcDir, f), 'utf8').split('\n');
  let i = 0;
  // heading
  while (lines[i].trim() === '') i++;
  const back = f.startsWith('back-');
  const m = back ? /^## (.+)$/.exec(lines[i].trim()) : /^## (Chapter \d+|Epilogue)$/.exec(lines[i].trim());
  if (!m) throw new Error('no heading in ' + f);
  i++;
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: children.length > 0,
    children: [new TextRun(smart(m[1]))],
  }));
  if (back) {
    stats.back++;
  } else {
    while (lines[i].trim() === '') i++;
    const n = /^\*\*(Jo|Cal)\*\*$/.exec(lines[i].trim());
    if (!n) throw new Error('no narrator in ' + f);
    i++;
    children.push(new Paragraph({ style: 'VellumElementSubtitle', children: [new TextRun(n[1])] }));
    // in a chapter where Jo strikes a line of the list, that line comes next, struck: "~~1. 5'8″ or taller~~".
    // Vellum drops strikethrough in a chapter subtitle, so it opens the chapter as a one-line Written Note
    // (body text keeps the strike, as on The List page; the drop cap still lands on the first paragraph)
    while (lines[i].trim() === '') i++;
    if (/^~~[^~]+~~$/.test(lines[i].trim())) {
      children.push(new Paragraph({ style: 'VellumWrittenNote', children: runsFromInline(lines[i].trim()) }));
      stats.struck = (stats.struck || 0) + 1;
      i++;
    }
    stats.chapters++;
  }

  while (i < lines.length) {
    const line = lines[i];
    if (line.trim() === '') { i++; continue; }
    if (line.trim() === '```') {
      const block = [];
      i++;
      while (lines[i].trim() !== '```') { block.push(lines[i]); i++; }
      i++;
      // cue cards and hand-written cards; phone and Remy screens stay monospace
      const isNote = block[0].startsWith('JOANNA SILVEIRA') || block[0].startsWith('JO SILVEIRA') || block[0].trim() === 'OWEN';
      for (const b of block) {
        if (b.trim() === '') continue;            // an empty paragraph would import as a scene break
        const text = smart(b.trim());
        if (isNote) {
          children.push(new Paragraph({ style: 'VellumWrittenNote', children: [new TextRun(text)] }));
        } else {
          children.push(new Paragraph({ style: 'VellumFlushLeft', children: [new TextRun({ text, style: 'VellumMonospace' })] }));
        }
        stats.words += b.trim().split(/\s+/).length;
      }
      if (isNote) stats.notes++; else stats.screens++;
      continue;
    }
    if (line.trim() === '***') {
      // Vellum turns three asterisks centered on their own line into an ornamental break
      children.push(new Paragraph({ alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, children: [new TextRun('***')] }));
      stats.breaks++;
      i++;
      continue;
    }
    if (back && line.startsWith('### ')) {
      children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(smart(line.slice(4).trim()))] }));
      i++;
      continue;
    }
    const img = back ? /^!\[(.*)\]\((.+\.(png|jpe?g))\)$/.exec(line.trim()) : null;
    if (img) {
      // a full-page picture, fit inside a 6.5 by 7.2 inch frame under the heading (96 px to the inch)
      const data = fs.readFileSync(path.join(srcDir, img[2]));
      let w = 2, h = 3;                                   // jpg: assume 2:3 portrait
      if (img[3] === 'png') { w = data.readUInt32BE(16); h = data.readUInt32BE(20); }
      const scale = Math.min(624 / w, 691 / h);
      // single auto spacing, so the 1.5-line body spacing cannot clip the picture
      children.push(new Paragraph({ alignment: AlignmentType.CENTER, indent: { firstLine: 0 }, spacing: { line: 240, lineRule: 'auto', before: 0, after: 0 }, children: [new ImageRun({
        type: img[3] === 'png' ? 'png' : 'jpg', data,
        transformation: { width: Math.round(w * scale), height: Math.round(h * scale) },
        altText: { title: img[1], description: img[1], name: path.basename(img[2]) },
      })] }));
      stats.images = (stats.images || 0) + 1;
      i++;
      continue;
    }
    if (back && line.startsWith('- ')) {
      children.push(new Paragraph({ bullet: { level: 0 }, children: runsFromInline(line.slice(2).trim()) }));
      stats.paragraphs++;
      stats.words += line.replace(/[*~]/g, '').trim().split(/\s+/).length - 1;
      i++;
      continue;
    }
    children.push(new Paragraph(Object.assign({ children: runsFromInline(line) }, back ? { style: 'BackMatterText' } : {})));
    stats.paragraphs++;
    stats.words += line.replace(/[*~]/g, '').trim().split(/\s+/).length;
    i++;
  }
}

const doc = new Document({
  creator: 'Wendy Garrity',
  title: 'Nobody Marries the List',
  description: 'Chapters 1 to 36 and the epilogue, first draft. Laid out for Vellum import.',
  styles: {
    default: { document: { run: { font: 'Times New Roman', size: 24 } } },
    paragraphStyles: [
      { id: 'Normal', name: 'Normal', run: { font: 'Times New Roman', size: 24 }, paragraph: { spacing: { line: 360 }, indent: { firstLine: 360 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true }, paragraph: { spacing: { before: 480, after: 360 }, indent: { firstLine: 0 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true }, paragraph: { spacing: { before: 360, after: 240 }, indent: { firstLine: 0 }, outlineLevel: 1 } },
      { id: 'VellumElementSubtitle', name: 'Vellum Element Subtitle', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28 }, paragraph: { indent: { firstLine: 0 }, spacing: { after: 360 } } },
      { id: 'VellumWrittenNote', name: 'Vellum Written Note', basedOn: 'Normal', quickFormat: true,
        paragraph: { indent: { left: 720, firstLine: 0 }, spacing: { line: 300 } }, run: { italics: true } },
      { id: 'BackMatterText', name: 'Back Matter Text', basedOn: 'Normal', quickFormat: true,
        paragraph: { indent: { firstLine: 0 }, spacing: { after: 120 } } },
      { id: 'VellumFlushLeft', name: 'Vellum Flush Left', basedOn: 'Normal', quickFormat: true,
        paragraph: { indent: { left: 720, firstLine: 0 }, spacing: { line: 300 } } },
    ],
    characterStyles: [
      { id: 'VellumMonospace', name: 'Vellum Monospace', run: { font: 'Courier New', size: 21 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outFile, buf);
  console.log(JSON.stringify(stats));
});
