export default function AppShell({ role, onRoleChange, children }) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Seyal AI Layer</p>
          <h1>Seyalla</h1>
        </div>
        <div className="role-switcher">
          <label htmlFor="role">View as</label>
          <select id="role" value={role} onChange={(e) => onRoleChange(e.target.value)}>
            <option value="admin">Admin</option>
            <option value="staff">Staff</option>
          </select>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
