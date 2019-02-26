#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const fetch = require('node-fetch');

const outdir = process.argv[2];
const stdin = fs.readFileSync(0, 'utf-8');
const config = JSON.parse(stdin);

const bookId = config.source.book_id;
const version = config.version.version;

const endpoint = `https://archive.cnx.org/contents/${bookId}@${version}.json`;

const writeFiles = book => {

  const meta = path.resolve(outdir, 'resource')
  fs.mkdirSync(meta);

  const metaBookFile = path.resolve(meta, 'book.json');
  const metaBookIdFile = path.resolve(meta, 'book-id.txt');
  const metaBookVersionFile = path.resolve(meta, 'book-version.txt');

  fs.writeFileSync(metaBookFile, JSON.stringify(book));
  fs.writeFileSync(metaBookIdFile, book.id);
  fs.writeFileSync(metaBookVersionFile, book.version);

  return book;
};

const writeOut = result => {
  process.stdout.write(JSON.stringify(result));
};


fetch(endpoint)
  .then(response => response.json())
  .then(writeFiles)
  .then(book => ({
    version: {
      version: book.version,
    },
    metadata: Object.entries(book)
      .filter(entry => ['title', 'version', 'created', 'baked', 'shortId', 'id', 'revised'].indexOf(entry[0]) > -1)
      .map(([name, value]) => ({name, value: '' + value}))
  }))
  .then(writeOut)
;
