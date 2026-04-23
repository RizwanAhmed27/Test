-- Seyalla PostgreSQL/Supabase-friendly schema (v1)

create table if not exists stores (
    store_id text primary key,
    name text not null,
    weekly_target numeric(12,2) not null
);

create table if not exists users (
    user_id text primary key,
    role text not null check (role in ('staff','admin')),
    name text not null,
    store_id text not null references stores(store_id)
);

create table if not exists sales_transactions (
    transaction_id text primary key,
    staff_id text not null references users(user_id),
    store_id text not null references stores(store_id),
    amount numeric(12,2) not null,
    business_date date not null
);

create table if not exists attendance (
    attendance_id text primary key,
    staff_id text not null references users(user_id),
    business_date date not null,
    status text not null check (status in ('present','absent','late')),
    hours numeric(5,2) not null default 0
);

create table if not exists targets (
    target_id text primary key,
    staff_id text not null references users(user_id),
    period text not null check (period in ('daily','weekly','monthly')),
    period_start date not null,
    target_amount numeric(12,2) not null
);

create table if not exists commission_rules (
    key text primary key,
    value numeric(12,4) not null
);

-- Seed examples
insert into stores (store_id, name, weekly_target) values
('s1', 'Downtown', 12000.00),
('s2', 'Mall', 9000.00)
on conflict do nothing;

insert into users (user_id, role, name, store_id) values
('staff_anna', 'staff', 'Anna', 's1'),
('staff_liam', 'staff', 'Liam', 's1'),
('staff_noor', 'staff', 'Noor', 's2'),
('mgr_s1', 'admin', 'Maria', 's1'),
('admin_root', 'admin', 'Root Admin', 's1')
on conflict do nothing;
