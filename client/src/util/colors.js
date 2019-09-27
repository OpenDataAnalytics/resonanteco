import * as d3 from "d3";

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
      "microbial mat",
      "marine pelagic zone",
      "marine oxygen minimum zone",
      "freshwater lake",
      "epilimnion"
    ],
    interpolateGreens: ["grassland biome", "farm", "sphagnum bog", "watershed"]
  },
  material: {
    interpolateBlues: [
      "coastal sea water",
      "sea water",
      "microbial mat material",
      "deep marine sediment",
      "fresh water",
      "hypersaline water"
    ],
    interpolateGreens: ["soil", "grassland soil", "farm soil"]
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
    interpolateGreens: [
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
