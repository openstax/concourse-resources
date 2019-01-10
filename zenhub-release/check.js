#!/usr/bin/env node

const fs = require("fs");
const fetch = require("node-fetch");

const stdin = fs.readFileSync(0, 'utf-8');
const source = JSON.parse(stdin);

const token = source.source.token;
const repo = source.source.repository_id;

const endpoint = `https://api.zenhub.io/p1/repositories/${repo}/reports/releases`;
const headers = {
  'X-Authentication-Token': token
}

const filterOpen = releases => releases.filter(release => release.state === 'open');
const filterAfter = releases => {
  const version = source.version;

  if (version) {
    return releases.slice(releases.findIndex(release => release.release_id === version.id));
  } else {
    return releases.slice(-1);
  }
};
const mapIds = releases => releases.map(release => ({id: release.release_id}));
const writeOut = releases => process.stdout.write(JSON.stringify(releases));

fetch(endpoint, {headers})
  .then(response => response.json())
  .then(filterOpen)
  .then(filterAfter)
  .then(mapIds)
  .then(ids => ids.reverse()) // concourse expects newer at the top
  .then(writeOut)
;
