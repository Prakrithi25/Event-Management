function generateImageLinksFromFolder() {
  const folderId = "1XW_KrZpKXHd_e2ATerJr9im_gy58f4ic"; // Replace this with your real folder ID
  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFiles();

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear(); // Clears old data
  sheet.appendRow(["Filename", "Direct Image Link"]);

  while (files.hasNext()) {
    const file = files.next();
    const name = file.getName();
    const id = file.getId();
    const directLink = "https://drive.google.com/uc?export=view&id=" + id;
    sheet.appendRow([name, directLink]);
  }
}
