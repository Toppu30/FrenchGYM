document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('toggleColumns'); // แก้ไข: เพิ่มเครื่องหมายคำพูดและแก้ไขไอดี
  toggle.addEventListener('change', function() {
    const table = document.getElementById('membersTable');
    const isHidden = !this.checked;
    Array.from(table.rows).forEach(row => {
      row.cells[row.cells.length - 3].style.display = isHidden ? 'none' : ''; // แก้ไข: ลบคำสั่งไม่จำเป็น
      row.cells[row.cells.length - 2].style.display = isHidden ? 'none' : ''; // แก้ไข: ลบคำสั่งไม่จำเป็น
      row.cells[row.cells.length - 1].style.display = isHidden ? 'none' : ''; // แก้ไข: ลบคำสั่งไม่จำเป็น
    });
  });
});
