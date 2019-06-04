export default function(handler) {
  var timeoutHandler = null;
  var events = [];
  return function(...args) {
    events.push(args);
    clearTimeout(timeoutHandler);
    timeoutHandler = setTimeout(() => {
      handler([...events]);
      events = [];
    }, 0);
  };
}
