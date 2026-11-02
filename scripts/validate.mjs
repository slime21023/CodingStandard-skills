import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const skillsDir = path.join(rootDir, 'skills');

console.log('🔍 Validating Agent Skills in:', skillsDir);

if (!fs.existsSync(skillsDir)) {
  console.error('❌ "skills/" directory not found!');
  process.exit(1);
}

const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
let hasErrors = false;
let validatedCount = 0;

for (const entry of entries) {
  if (!entry.isDirectory()) continue;
  const skillName = entry.name;
  const skillPath = path.join(skillsDir, skillName);
  const skillMdPath = path.join(skillPath, 'SKILL.md');

  console.log(`\n📁 Checking [${skillName}]...`);

  // 1. Check SKILL.md
  if (!fs.existsSync(skillMdPath)) {
    console.error(`  ❌ Missing SKILL.md in ${skillName}`);
    hasErrors = true;
    continue;
  }

  const content = fs.readFileSync(skillMdPath, 'utf8');

  // 2. Validate Frontmatter
  const frontmatterMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatterMatch) {
    console.error(`  ❌ Invalid or missing YAML frontmatter in ${skillName}/SKILL.md`);
    hasErrors = true;
    continue;
  }

  const frontmatter = frontmatterMatch[1];
  const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
  const name = nameMatch ? nameMatch[1].trim() : null;

  if (!name) {
    console.error(`  ❌ Missing "name" field in frontmatter`);
    hasErrors = true;
  } else if (name !== skillName) {
    console.error(`  ❌ Frontmatter name "${name}" does not match folder name "${skillName}"`);
    hasErrors = true;
  }

  const descMatch = frontmatter.match(/^description:\s*([\s\S]*?)(?=^\w+:|$)/m);
  const rawDesc = descMatch ? descMatch[1].trim() : null;
  if (!rawDesc) {
    console.error(`  ❌ Missing "description" field in frontmatter`);
    hasErrors = true;
  } else if (rawDesc.length > 1024) {
    console.warn(`  ⚠️ Warning: Description is ${rawDesc.length} chars (recommended <= 1024)`);
  }

  // 3. Validate relative links
  const linkMatches = content.matchAll(/\[.*?\]\((.*?)\)/g);
  for (const m of linkMatches) {
    const targetLink = m[1].split('#')[0]; // strip anchors
    if (!targetLink || targetLink.startsWith('http://') || targetLink.startsWith('https://') || targetLink.startsWith('mailto:')) {
      continue;
    }
    const resolvedTarget = path.resolve(skillPath, targetLink);
    if (!fs.existsSync(resolvedTarget)) {
      console.error(`  ❌ Broken relative link in ${skillName}/SKILL.md: "${targetLink}"`);
      hasErrors = true;
    }
  }

  // 4. Validate agents/openai.yaml if present
  const openaiYamlPath = path.join(skillPath, 'agents', 'openai.yaml');
  if (fs.existsSync(openaiYamlPath)) {
    const yamlContent = fs.readFileSync(openaiYamlPath, 'utf8');
    if (!yamlContent.includes('interface:') || !yamlContent.includes('display_name:')) {
      console.warn(`  ⚠️ Warning: agents/openai.yaml exists but may be missing standard fields.`);
    }
  }

  if (!hasErrors) {
    console.log(`  ✅ Valid skill (${skillName})`);
    validatedCount++;
  }
}

console.log('\n========================================');
if (hasErrors) {
  console.error(`❌ Validation failed with errors.`);
  process.exit(1);
} else {
  console.log(`🎉 All ${validatedCount} skills passed validation successfully!`);
}
