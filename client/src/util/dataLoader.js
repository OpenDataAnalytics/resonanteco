import Papa from "papaparse";

import summaryText from "../data/NGEE_ResEco_36metagenomes_IMGM_summary.txt";
import metaText from "../data/NGEE_ResEco_36metagenomes_meta.txt";

var summary = Papa.parse(summaryText, { header: true, skipEmptyLines: true })
  .data;
var meta = Papa.parse(metaText, { header: true, skipEmptyLines: true }).data;
import table7Texts from "../data/table7";
import table8Texts from "../data/table8";
import table9Texts from "../data/table9";

var table7 = thatFormatReader(table7Texts);
var table8 = thatFormatReader(table8Texts);
var table9 = thatFormatReader(table9Texts);

var dataset = {
  summary,
  meta,
  table7,
  table8,
  table9
};

function thatFormatReader(tableTexts) {
  var table = {};
  for (let [tableAndSampleId, text] of Object.entries(tableTexts)) {
    let sampleId = tableAndSampleId.split("_")[1];
    let lines = text.split(/\r?\n/);
    var map = {};
    for (var i = 3; i < lines.length; i++) {
      let line = lines[i];
      let splits = line.split("  ");
      var key = splits[0];
      if (key) {
        var value = splits.slice(-1)[0].trim();
        var parseResult = parseFloat(value);
        if (!isNaN(parseResult)) {
          value = parseResult;
        }
        map[key] = value;
      }
    }
    table[sampleId] = map;
  }
  return table;
}

export { dataset };
