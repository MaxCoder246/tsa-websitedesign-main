const express = require("express");

const app = express();
const PORT = process.env.PORT || 8080;

app.set("view engine", "ejs");
app.set("views", "./views");

app.use(express.json());
app.use(express.static("public"));

app.get("/", (_req, res) => {
  res.render("index", {
    title: "Our Basking Ridge Community",
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
