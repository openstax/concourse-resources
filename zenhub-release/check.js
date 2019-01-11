#!/usr/bin/env node

const fs = require("fs");
const fetch = require("node-fetch");

const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const token = config.source.token;
const repo = config.source.repository_id;

const endpoint = `https://api.zenhub.io/p1/repositories/${repo}/reports/releases`;
const headers = {
  'X-Authentication-Token': token
}

const filterOpen = releases => releases.filter(release => release.state === 'open');
const filterAfter = releases => {
  const version = config.version;

  if (version) {
    return releases.slice(releases.findIndex(release => release.release_id === version.id));
  } else {
    return releases.slice(-1);
  }
};
const mapIds = releases => releases.map(release => ({id: release.release_id}));
const writeOut = releases => process.stdout.write(JSON.stringify(releases));

const request = fetch(endpoint, {headers})
  .then(response => response.json())
  .then(filterOpen)
;

if (config.source.mode === 'multiple') {
  request
    .then(releases => releases.reduce((ids, release) => {
      ids.push(release.release_id);
      return ids;
    }, []))
    .then(ids => ([{ids: ids.join(',')}]))
    .then(writeOut)
  ;
} else {
  request
    .then(filterAfter)
    .then(mapIds)
    .then(ids => ids.reverse()) // concourse expects newer at the top
    .then(writeOut)
  ;
}
