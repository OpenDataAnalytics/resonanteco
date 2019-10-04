import * as d3 from "d3";

// console.log(d3.interpolateRgb("brown", "red"));
// d3.interpolateBrown = d3.interpolateRgb("brown", "red");

function colorScale(values, interpolator) {
  var scale = d3.scaleSequential(interpolator);
  return function(value) {
    var index = values.indexOf(value);
    return scale(0.5 + 0.5 * (index / values.length));
  };
}

var colormap = {
  feature: {
    interpolateBlues: [
      null,
      "bay",
      "coastal inlet",
      "marine pelagic biome",
      "ocean biome",
      "marine pelagic zone",
      "marine oxygen minimum zone",
      "freshwater lake",
      "epilimnion"
    ],
    interpolateOranges: ["grassland biome", "farm", "sphagnum bog", "watershed"],
    interpolateRdPu:["microbial mat"]
  },
  material: {
    interpolateBlues: [
      "coastal sea water",
      "sea water",
      "deep marine sediment",
      "fresh water",
      "hypersaline water"
    ],
    interpolateOranges: ["soil", "grassland soil", "farm soil"],
    interpolateRdPu:["microbial mat material"]
  },
  biome: {
    interpolateBlues: [
      "arctic",
      "marine biome",
      "alkaline hot spring",
      "marine benthic biome",
      "ocean biome",
      "marine oxygen minimum zone",
      "freshwater lake biome",
      "hypersaline lake"
    ],
    interpolateOranges: [
      "terrestrial biome",
      "anthropogenic terrestrial biome",
      "grassland biome",
      "terrestrial biome"
    ]
  }
};

var mapColor = (function() {
  var mappers = {};
  for (let category in colormap) {
    mappers[category] = {};
    for (let interpolatorName in colormap[category]) {
      mappers[category][interpolatorName] = colorScale(
        colormap[category][interpolatorName],
        d3[interpolatorName]
      );
    }
  }

  return function(category, name) {
    for (let interpolatorName in colormap[category]) {
      if (colormap[category][interpolatorName].indexOf(name) !== -1) {
        return mappers[category][interpolatorName](name);
      }
    }
    return "red";
  };
})();

export { colorScale, colormap, mapColor };
