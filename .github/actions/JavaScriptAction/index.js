const core = require('@actions/core');

try {
  // 1. Get the input defined in action.yml
  const nameToGreet = core.getInput('my_name');
  
  console.log(`Hello ${nameToGreet}!`);

  // 2. Set the output defined in action.yml
  const greeting = `Hello ${nameToGreet}`;
  core.setOutput("greeting", greeting);

} catch (error) {
  // 3. Handle errors and fail the step if necessary
  core.setFailed(error.message);
}
