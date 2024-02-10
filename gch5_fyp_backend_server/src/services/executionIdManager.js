let executionId = null;

const generateExecutionId = () => {
    // Simple example: Use current timestamp as executionId
    executionId = `exec-${Date.now()}`;
    return executionId;
};

const getExecutionId = () => executionId;

module.exports = { generateExecutionId, getExecutionId };