const toast = document.querySelector('#toast');
let emergencyStopActive = false;

// Auto-detect API URL: local for development, production for deployed
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
  ? 'http://127.0.0.1:8000' 
  : window.location.origin.replace(/:\d+$/, '');

console.log('API Base URL:', API_BASE);

function showToast(message) { toast.textContent = message; toast.classList.add('show'); window.setTimeout(() => toast.classList.remove('show'), 2800); }

document.querySelector('#killSwitch').addEventListener('click', () => { emergencyStopActive = true; document.querySelector('#killSwitch').textContent = 'Stop active'; showToast('Emergency stop active. New paper trades blocked.'); });
document.querySelector('#tradeBtn').addEventListener('click', async () => {
  if (emergencyStopActive) { showToast('Order blocked by emergency stop.'); return; }
  const order = { symbol: 'RELIANCE', side: 'BUY', quantity: 100, entry_price: 1462, stop_loss: 1438, virtual_capital: 100000, risk_per_trade_percent: 0.5, confirmed: true, trading_mode: 'PAPER' };
  try {
    const response = await fetch(API_BASE + '/trade', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(order) });
    if (!response.ok) throw new Error('backend unavailable');
    const result = await response.json(); showToast(`${result.status}: ${result.quantity} RELIANCE shares approved`);
  } catch { showToast('Backend is offline. Start FastAPI to simulate an order.'); }
});
document.querySelectorAll('.segmented button').forEach(button => button.addEventListener('click', () => { document.querySelector('.segmented .selected').classList.remove('selected'); button.classList.add('selected'); showToast(`Performance range: ${button.textContent}`); }));

const updateSignalButtons = (mode) => {
  const freeBtn = document.getElementById('signalFreeBtn');
  const paidBtn = document.getElementById('signalPaidBtn');
  const signalMode = document.getElementById('signalMode');
  const isFree = mode === 'FREE';
  freeBtn.classList.toggle('on', isFree);
  freeBtn.classList.toggle('disabled', !isFree);
  paidBtn.classList.toggle('on', !isFree);
  paidBtn.classList.toggle('disabled', isFree);
  if (signalMode) signalMode.value = mode;
};

document.getElementById('signalFreeBtn').addEventListener('click', () => updateSignalButtons('FREE'));
document.getElementById('signalPaidBtn').addEventListener('click', () => updateSignalButtons('PAID'));

document.getElementById('signalForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = {
    mode: document.getElementById('signalMode').value,
    provider: document.getElementById('signalProvider').value,
    api_key: document.getElementById('signalApiKey').value,
    notes: document.getElementById('signalNotes').value,
  };
  try {
    const response = await fetch(API_BASE + '/signals/config', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Signal config failed');
    updateSignalButtons(result.mode);
    showToast(`${result.mode} signal mode saved`);
    document.getElementById('signalForm').reset();
  } catch (error) { showToast(error.message || 'Signal config failed.'); }
});

document.getElementById('userForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = {
    full_name: document.getElementById('fullName').value,
    username: document.getElementById('username').value,
    password: document.getElementById('password').value,
  };
  try {
    const response = await fetch(API_BASE + '/users/register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Unable to create user');
    showToast(`User created: ${result.username}`);
    document.getElementById('userForm').reset();
  } catch (error) { showToast(error.message || 'User creation failed.'); }
});

document.getElementById('brokerForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = {
    broker_name: document.getElementById('brokerName').value,
    api_key: document.getElementById('brokerApiKey').value,
    api_secret: document.getElementById('brokerApiSecret').value,
    demat_account: document.getElementById('dematAccount').value,
    account_number: document.getElementById('accountNumber').value,
  };
  try {
    const response = await fetch(API_BASE + '/broker/connect', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Broker connection failed');
    showToast(`Broker connected: ${result.broker_name}`);
    document.getElementById('brokerForm').reset();
  } catch (error) { showToast(error.message || 'Broker setup failed.'); }
});

document.getElementById('liveTradeForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const checkbox = document.getElementById('realMoneyAcknowledge').checked;
  const code = document.getElementById('liveTradeCode').value.trim();
  if (!checkbox) { showToast('Please acknowledge the risks before enabling live trading'); return; }
  if (code !== 'ENABLE-LIVE-TRADING') { showToast('Incorrect approval code. Use: ENABLE-LIVE-TRADING'); return; }
  const payload = { approved: true, approval_code: code };
  try {
    const response = await fetch(API_BASE + '/live-trading/approve', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Live trading approval failed');
    showToast('✓ Real-money trading ENABLED. Use with caution.');
    document.getElementById('liveTradeForm').reset();
  } catch (error) { showToast(error.message || 'Live trading approval failed.'); }
});

document.getElementById('realMoneyAcknowledge').addEventListener('change', (event) => {
  document.getElementById('liveTradeSubmit').disabled = !event.target.checked;
});

document.querySelectorAll('[data-setting]').forEach(button => button.addEventListener('click', () => {
  const setting = button.dataset.setting;
  if (setting === 'Daily P&L report') { showToast('Daily report will be available after trade history storage is connected.'); return; }
  if (setting === 'Real-money trading') { showToast('Real-money trading is locked until broker API setup, risk review, and approval are complete.'); return; }
  if (setting === 'Demat / broker connection' || setting === 'Live broker credentials') { showToast('Broker or Demat setup is disabled for safety. Enable only after your review and approval.'); return; }
  if (setting === 'Broker connection') { showToast('Broker connection is locked until an official API is configured.'); return; }
  showToast(`${setting} settings will open when configuration storage is connected.`);
}));

updateSignalButtons('FREE');
