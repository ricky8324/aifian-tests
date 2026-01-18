import { test as setup } from '@playwright/test';
import { urlPaths } from '../constant';
import path from 'path';
import fs from 'fs';

setup('get x-aifian-token', async ({ request }) => {
  try {
    // find the store folder
    const rootDir = path.join(__dirname, '../store');
    const stateFile = path.join(rootDir, 'config.json');

    // call config api
    const response = await request.get(urlPaths.config);
    if (!response.ok()) {
      throw new Error(`Failed to fetch config API: ${response.status()}`);
    }

    const data = await response.json();

    await fs.promises.mkdir(rootDir, { recursive: true }); // create the store folder if it doesn't exist
    await fs.promises.writeFile(
      stateFile,
      JSON.stringify({ token: data.token }, null, 2),
      'utf8',
    );
  } catch (error) {
    console.error('Error fetching config:', error);
    throw error;
  }
});
