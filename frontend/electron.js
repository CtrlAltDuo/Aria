const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    titleBarStyle: 'hiddenInset',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  // Start the Python backend
  const fs = require('fs');
  const venvPythonPath = path.join(__dirname, '..', 'backend', 'venv', 'bin', 'python3');
  const pythonCmd = fs.existsSync(venvPythonPath) ? venvPythonPath : 'python3';
  
  pythonProcess = spawn(pythonCmd, ['-m', 'uvicorn', 'backend.main:app', '--reload', '--port', '8000'], {
    cwd: path.join(__dirname, '..')
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Backend stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Backend stderr: ${data}`);
  });

  // In dev mode, wait for Vite to be ready and load the URL
  // The wait-on package in package.json handles the wait
  mainWindow.loadURL('http://localhost:5173');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});
