const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('electronAPI', {
  openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),
  onMenuOpenReport: (cb) => ipcRenderer.on('menu-open-report', cb),
  onMenuCloseReport: (cb) => ipcRenderer.on('menu-close-report', cb),
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
})
