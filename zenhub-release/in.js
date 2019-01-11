#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const outdir = process.argv[2];
const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const token = config.source.token;
const repo = config.source.repository_id;
const headers = {
  'X-Authentication-Token': token
}

const writeFiles = dest => release => {
  const jsonFile = path.resolve(dest, 'release.json');
  const titleFile = path.resolve(dest, 'title.txt');
  const idFile = path.resolve(dest, 'id.txt');

  fs.writeFileSync(jsonFile, JSON.stringify(release), 'utf-8');
  fs.writeFileSync(titleFile, release.title, 'utf-8');
  fs.writeFileSync(idFile, release.release_id, 'utf-8');

  return release;
};

const writeOut = result => {
  process.stdout.write(JSON.stringify(result));
};

if (config.source.mode === 'multiple') {
  const versions = config.version.ids.split(',');
  const endpoint = `https://api.zenhub.io/p1/repositories/${repo}/reports/releases`;
  const request = fetch(endpoint, {headers})
    .then(response => response.json())
    .then(releases => releases.filter(release => versions.indexOf(release.release_id) > -1))
    .then(releases => {
      releases.forEach(release => writeFiles(path.resolve(outdir, release.release_id)));
      return releases;
    })
    .then(releases => ({
      version: config.version,
      metadata: releases.map(release => ({name: release.release_id, value: release.title}))
    }))
    .then(writeOut)
  ;
} else {
  const version = config.version.id;
  const endpoint = `https://api.zenhub.io/p1/reports/release/${version}`;

  fetch(endpoint, {headers})
    .then(response => response.json())
    .then(writeFiles(outdir))
    .then(release => ({
      version: {
        id: release.release_id,
      },
      metadata: Object.entries(release)
        .map(([name, value]) => ({name, value}))
        .filter(meta => ['string', 'number'].indexOf(typeof(meta.value)) > -1)
    }))
    .then(writeOut)
  ;
}
