// Build a Word file laid out for Vellum import from the chapter markdown files.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');

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
  // *italic* spans only
  const parts = text.split('*');
  if (parts.length % 2 === 0) throw new Error('unbalanced * in: ' + text.slice(0, 60));
  const runs = [];
  parts.forEach((p, i) => {
    if (p === '') return;
    runs.push(new TextRun(Object.assign({ text: smart(p), italics: i % 2 === 1 }, extra || {})));
  });
  return runs;
}

const files = fs.readdirSync(srcDir).filter(f => /^chapter-\d\d-(jo|cal)\.md$/.test(f)).sort();
const children = [];
const stats = { chapters: 0, paragraphs: 0, notes: 0, screens: 0, breaks: 0, words: 0 };

for (const f of files) {
  const lines = fs.readFileSync(path.join(srcDir, f), 'utf8').split('\n');
  let i = 0;
  // heading
  while (lines[i].trim() === '') i++;
  const m = /^## Chapter (\d+)$/.exec(lines[i].trim());
  if (!m) throw new Error('no heading in ' + f);
  i++;
  while (lines[i].trim() === '') i++;
  const n = /^\*\*(Jo|Cal)\*\*$/.exec(lines[i].trim());
  if (!n) throw new Error('no narrator in ' + f);
  i++;
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: stats.chapters > 0,
    children: [new TextRun('Chapter ' + m[1])],
  }));
  children.push(new Paragraph({ style: 'VellumElementSubtitle', children: [new TextRun(n[1])] }));
  stats.chapters++;

  while (i < lines.length) {
    const line = lines[i];
    if (line.trim() === '') { i++; continue; }
    if (line.trim() === '```') {
      const block = [];
      i++;
      while (lines[i].trim() !== '```') { block.push(lines[i]); i++; }
      i++;
      const isNote = block[0].startsWith('JOANNA SILVEIRA');
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
    children.push(new Paragraph({ children: runsFromInline(line) }));
    stats.paragraphs++;
    stats.words += line.replace(/\*/g, '').trim().split(/\s+/).length;
    i++;
  }
}

const doc = new Document({
  creator: 'Wendy Garrity',
  title: 'Nobody Marries the List',
  description: 'Chapters 1 to 10, first draft. Laid out for Vellum import.',
  styles: {
    default: { document: { run: { font: 'Times New Roman', size: 24 } } },
    paragraphStyles: [
      { id: 'Normal', name: 'Normal', run: { font: 'Times New Roman', size: 24 }, paragraph: { spacing: { line: 360 }, indent: { firstLine: 360 } } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true }, paragraph: { spacing: { before: 480, after: 360 }, indent: { firstLine: 0 }, outlineLevel: 0 } },
      { id: 'VellumElementSubtitle', name: 'Vellum Element Subtitle', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28 }, paragraph: { indent: { firstLine: 0 }, spacing: { after: 360 } } },
      { id: 'VellumWrittenNote', name: 'Vellum Written Note', basedOn: 'Normal', quickFormat: true,
        paragraph: { indent: { left: 720, firstLine: 0 }, spacing: { line: 300 } }, run: { italics: true } },
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
