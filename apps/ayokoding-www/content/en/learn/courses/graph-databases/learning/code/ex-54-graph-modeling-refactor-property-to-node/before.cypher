// Example 54a: city as a plain PROPERTY -- cannot carry its own attributes.
CREATE (:Person {name: 'Ada', city: 'Berlin'});
// => "Berlin" is just a string -- there is nowhere to attach a population or a timezone to it
