const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/home/ubuntu/.openclaw/media/inbound/76238e1c-81f6-4698-8f56-3df1f6480c42.json', 'utf8'));

data.forEach((item, index) => {
    const title = item.title || `Meeting ${index + 1}`;
    const summary = item.summary || '';
    const safeName = title.replace(/[\/\\:*?"<>|]/g, '-').substring(0, 80);
    
    let mdContent = `# ${title}\n\n`;
    if (item.summary) {
        mdContent += item.summary;
    } else {
        mdContent += '_No summary available_\n';
    }
    
    fs.writeFileSync(`./${String(index + 1).padStart(3, '0')}-${safeName}.md`, mdContent);
    console.log(`Created: ${index + 1}-${safeName}.md`);
});

console.log(`\nTotal: ${data.length} files created`);
