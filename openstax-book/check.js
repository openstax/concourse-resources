#!/usr/bin/env node

const fs = require("fs");
const fetch = require("node-fetch");

const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const bookId = config.source.book_id;

const endpoint = `https://archive.cnx.org/contents/${bookId}.json`;

const filterAfter = versions => {
  const after = config.version;

  if (after) {
    return versions.slice(0, versions.findIndex(existing => existing.version == after.version));
  } else {
    return versions.slice(0, 1);
  }
};

const writeOut = versions => process.stdout.write(JSON.stringify(versions));

const request = fetch(endpoint)
  .then(response => response.json())
  .then(book => book.history)
  .then(filterAfter)
  .then(versions => versions.map(({version}) => ({version})))
  .then(writeOut)
;
