#!/usr/bin/env node

const fs = require("fs");
const fetch = require("node-fetch");

const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const username = config.source.username;
const password = config.source.password;
const repo = config.source.repository;

const endpoint = `http://api.github.com/repos/${repo}/milestones`;
const headers = {
  'Authorization': 'Basic ' + Buffer.from(username + ':' + password).toString('base64')
}

const filterAfter = milestones => {
  const version = config.version;

  if (version) {
    return milestones.slice(milestones.findIndex(milestone => milestone.number == version.id));
  } else {
    return milestones.slice(-1);
  }
};

const writeOut = milestones => process.stdout.write(JSON.stringify(milestones));

const request = fetch(endpoint, {headers})
  .then(response => response.json())
;

if (config.source.mode === 'multiple') {
  request
    .then(milestones => milestones.reduce((ids, milestone) => ([...ids, milestone.number]), []))
    .then(ids => ([{ids: ids.join(',')}]))
    .then(writeOut)
  ;
} else {
  request
    .then(filterAfter)
    .then(milestones => milestones.map(milestone => ({id: milestone.number})))
    .then(ids => ids.reverse()) // concourse expects newer at the top
    .then(writeOut)
  ;
}
