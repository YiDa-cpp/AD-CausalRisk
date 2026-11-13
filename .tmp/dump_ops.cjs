const p = require('../contracts/java-business.target.openapi.json')
const rows = []
for (const [path, ops] of Object.entries(p.paths)) {
  for (const [m, op] of Object.entries(ops)) {
    if (!['get', 'post', 'patch', 'delete', 'put'].includes(m)) continue
    const params = (op.parameters || []).map((x) => x.name)
    const res = op.responses?.['200']?.content?.['application/json']?.schema
    let ref = ''
    if (res) {
      if (res.$ref) ref = res.$ref
      else if (res.properties?.data?.$ref) ref = res.properties.data.$ref
      else if (res.properties?.data?.items?.$ref) ref = res.properties.data.items.$ref
      else ref = JSON.stringify(res).slice(0, 60)
    }
    rows.push([m.toUpperCase(), path, op.operationId || '', params.join('|'), ref].join('\t'))
  }
}
rows.sort((a, b) => a.split('\t')[1].localeCompare(b.split('\t')[1]))
console.log(rows.join('\n'))
console.error('OPS=' + rows.length)
