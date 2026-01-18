import fs from 'fs';
import path from 'path';

export const getConfigToken = () => {
  try {
    const stateFile = path.join(__dirname, '../store/config.json');

    if (fs.existsSync(stateFile)) {
      const state = JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
      return state.token;
    }
    console.error('Config file not found, returning empty token');
  } catch (error) {
    console.error('Error reading config file:', error);
  }
};
