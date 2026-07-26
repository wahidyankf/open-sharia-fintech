// Example 41: Fraud Ring via a Shared Attribute. (co-16, co-08)
CREATE (a:Account {name: 'Acc-A'})-[:USES]->(d:Device {id: 'dev-42'})<-[:USES]-(b:Account {name: 'Acc-B'});
// => planted fraud ring: two DIFFERENT accounts both use the SAME device
CREATE (:Account {name: 'Acc-C'})-[:USES]->(:Device {id: 'dev-99'});
// => an unrelated account on its OWN device -- must NOT show up below

MATCH (a:Account)-[:USES]->(d:Device)<-[:USES]-(b:Account)
// => finds every (account, device, account) triple sharing a device, in EITHER direction
WHERE a <> b
// => excludes a device matching against ITSELF -- a real requirement, not decoration
RETURN a.name, b.name, d.id;
// => co-08: only the SHARED-device pair surfaces -- Acc-C's isolated device matches nothing
