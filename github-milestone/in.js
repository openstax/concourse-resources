#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const outdir = process.argv[2];
const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const username = config.source.username;
const password = config.source.password;
const repo = config.source.repository;

const endpoint = `http://api.github.com/repos/${repo}/milestones`;
const headers = {
  'Authorization': 'Basic ' + Buffer.from(username + ':' + password).toString('base64')
}

const writeFiles = dest => milestone => {
  const jsonFile = path.resolve(dest, 'milestone.json');
  const titleFile = path.resolve(dest, 'title.txt');
  const slugFile = path.resolve(dest, 'title-slug.txt');
  const numberFile = path.resolve(dest, 'number.txt');
  const idFile = path.resolve(dest, 'id.txt');

  fs.writeFileSync(jsonFile, JSON.stringify(milestone));
  fs.writeFileSync(titleFile, milestone.title);
  fs.writeFileSync(slugFile, milestone.title.replace(/(^[^a-z]{1})|([^a-z0-9 \-]+)|([^a-z0-9]+$)/g, '').replace(/[ \-]+/g, '-'));
  fs.writeFileSync(numberFile, milestone.number);
  fs.writeFileSync(idFile, milestone.id);

  return milestone;
};

const writeOut = result => {
  process.stdout.write(JSON.stringify(result));
};

if (config.source.mode === 'multiple') {
  const versions = config.version.ids.split(',');
  const request = fetch(endpoint, {headers})
    .then(response => response.json())
    .then(milestones => milestones.filter(milestone => versions.indexOf('' + milestone.number) > -1))
    .then(milestones => {
      milestones.forEach(milestone => {
        const dest = path.resolve(outdir, '' + milestone.number);
        fs.mkdirSync(dest);
        writeFiles(dest)(milestone);
      });
      return milestones;
    })
    .then(milestones => ({
      version: config.version,
      metadata: milestones.map(milestone => ({name: '' + milestone.number, value: milestone.title}))
    }))
    .then(writeOut)
  ;
} else {
  const version = config.version.id;

  fetch(`${endpoint}/${version}`, {headers})
    .then(response => response.json())
    .then(writeFiles(outdir))
    .then(milestone => ({
      version: {
        id: '' + milestone.number,
      },
      metadata: Object.entries(milestone)
        .filter(entry => ['string', 'number'].indexOf(typeof(entry[1])) > -1)
        .map(([name, value]) => ({name, value: '' + value}))
    }))
    .then(writeOut)
  ;
}
