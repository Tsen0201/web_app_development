/* ============================================
   任務管理系統 — 前端 JavaScript
   ============================================
   功能：
   1. 任務提醒通知檢查
   2. Flash 訊息自動消失
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // ----- 1. Flash 訊息 3 秒後自動消失 -----
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 3000);
    });

    // ----- 2. 任務提醒通知檢查 -----
    function checkReminders() {
        fetch('/api/reminders')
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (!data.reminders || data.reminders.length === 0) return;

                const now = new Date();

                data.reminders.forEach(function (task) {
                    if (!task.reminder_at) return;

                    const reminderTime = new Date(task.reminder_at);
                    const diffMinutes = (reminderTime - now) / (1000 * 60);

                    // 提醒時間已到或在 30 分鐘內
                    if (diffMinutes <= 30 && diffMinutes > -60) {
                        showReminderNotification(task, diffMinutes);
                    }
                });
            })
            .catch(function (err) {
                console.log('[提醒] 檢查失敗:', err);
            });
    }

    function showReminderNotification(task, diffMinutes) {
        // 避免重複提醒（用 sessionStorage 紀錄已提醒的任務 ID）
        var key = 'reminded_' + task.id;
        if (sessionStorage.getItem(key)) return;
        sessionStorage.setItem(key, 'true');

        var timeText;
        if (diffMinutes <= 0) {
            timeText = '⏰ 提醒時間已到！';
        } else {
            timeText = '⏰ 將在 ' + Math.round(diffMinutes) + ' 分鐘後到期';
        }

        // 建立 toast 通知
        var toastHtml =
            '<div class="toast show position-fixed bottom-0 end-0 m-3 shadow-lg" role="alert" style="z-index:9999;">' +
            '  <div class="toast-header bg-warning text-dark">' +
            '    <i class="bi bi-bell-fill me-2"></i>' +
            '    <strong class="me-auto">任務提醒</strong>' +
            '    <small>' + timeText + '</small>' +
            '    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>' +
            '  </div>' +
            '  <div class="toast-body">' +
            '    <strong>' + task.title + '</strong>' +
            '    <div class="mt-2">' +
            '      <a href="/tasks/' + task.id + '" class="btn btn-sm btn-primary">查看詳情</a>' +
            '    </div>' +
            '  </div>' +
            '</div>';

        var container = document.createElement('div');
        container.innerHTML = toastHtml;
        document.body.appendChild(container.firstElementChild);
    }

    // 啟動時檢查一次，之後每 60 秒檢查
    checkReminders();
    setInterval(checkReminders, 60000);

});
