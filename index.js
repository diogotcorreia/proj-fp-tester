const express = require("express");
const fs = require("fs").promises;
const bodyParser = require("body-parser");
const { v4: uuidv4 } = require("uuid");
const app = express();
const path = require("path");
const spawn = require("child_process").spawn;

app.use(bodyParser.text());

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/run", async (req, res) => {
  const uuid = uuidv4();
  const filePath = path.join(__dirname, "tests", `runner-${uuid}.py`);
  await fs.writeFile(filePath, req.body);

  const pythonProcess = spawn("python3", [
    path.join(__dirname, "tests", "test.py"),
    `runner-${uuid}`,
  ]);

  let result = "";

  pythonProcess.stdout.on("data", (data) => {
    result += data.toString() + "\n";
  });

  pythonProcess.stderr.on("data", (data) => {
    result += data.toString() + "\n";
  });

  pythonProcess.on("close", async () => {
    await fs.unlink(filePath);
    res.send(result);
  });
});

app.listen(process.env.PORT || 5000);
console.log(
  `Listening on port ${
    process.env.PORT || 5000
  }. You can change this by passing a value to the PORT environment variable.`
);
