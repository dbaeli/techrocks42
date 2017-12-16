let Wappalyzer = require('wappalyzer');
const options = {
  debug: false,
  delay: 500,
  maxDepth: 3,
  maxUrls: 10,
  maxWait: 1000,
  recursive: true,
  requestTimeout: 3000,
  userAgent: 'Wappalyzer',
};

const wappalyzer = new Wappalyzer(process.argv[2], options);

wappalyzer.analyze()
  .then(json => {
    process.stdout.write(JSON.stringify(json, null, 2) + '\n')
 
    process.exit(0);
  })
  .catch(error => {
    process.stderr.write(error + '\n')
 
    process.exit(1);
});

