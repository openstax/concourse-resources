#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const dest = process.argv[2];
const stdin = fs.readFileSync(0, 'utf-8');
const source = JSON.parse(stdin);

const token = source.source.token;
const repo = source.source.repository_id;
const version = source.version.id;

const endpoint = `https://api.zenhub.io/p1/reports/release/${version}`;
const headers = {
  'X-Authentication-Token': token
}

const writeFiles = release => {
  const jsonFile = path.resolve(dest, 'release.json');
  const titleFile = path.resolve(dest, 'title.txt');
  const idFile = path.resolve(dest, 'id.txt');

  fs.writeFileSync(jsonFile, JSON.stringify(release), 'utf-8');
  fs.writeFileSync(titleFile, release.title, 'utf-8');
  fs.writeFileSync(idFile, release.release_id, 'utf-8');

  return release;
};

const writeOut = release => {
  process.stdout.write(JSON.stringify({
    version: {
      id: release.release_id,
    },
    metadata: Object.entries(release)
      .map(([name, value]) => ({name, value}))
      .filter(meta => ['string', 'number'].indexOf(typeof(meta.value)) > -1)
  }));
};

fetch(endpoint, {headers})
  .then(response => response.json())
  .then(writeFiles)
  .then(writeOut)
;
