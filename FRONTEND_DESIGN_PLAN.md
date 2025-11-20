# Frontend Design Implementation Plan

Based on the design mockups provided, here is the work plan to transform the frontend into a modern, professional application using **React** and **Tailwind CSS**.

## 🎨 Design Analysis

**Visual Style:**
- **Theme**: Clean, Minimalist, Enterprise SaaS look.
- **Color Palette**:
  - **Primary**: Royal Blue (`#2563EB` or similar) for buttons and active states.
  - **Background**: Light Gray (`#F3F4F6`) for the main app background.
  - **Surface**: White (`#FFFFFF`) for cards and sidebar.
  - **Text**: Dark Slate (`#1E293B`) for headings, lighter gray for secondary text.
- **Typography**: Sans-serif (likely Inter or Roboto).
- **Layout**:
  - **Sidebar**: Fixed left navigation with logo, links, and user profile at bottom.
  - **Header**: Top bar with global search, notifications, and theme toggle.
  - **Content**: Card-based layout for data presentation.

---

## 🛠️ Tech Stack Additions

To achieve this look efficiently, we will add:
1.  **Tailwind CSS**: For utility-first styling (perfect match for this design).
2.  **Lucide React** or **Heroicons**: For the clean SVG icons shown in the sidebar.
3.  **Recharts**: For the "Sales Trends" curved line chart.
4.  **Clsx / Tailwind-merge**: For conditional class handling.

---

## 📅 Implementation Phases

### Phase 1: Foundation & Setup (Day 1)
**Goal**: Set up the styling engine and base components.

1.  **Install Tailwind CSS**
    -   Configure `tailwind.config.js` with custom colors from the design.
    -   Set up global font (Inter).
2.  **Install Icons & Charts**
    -   `npm install lucide-react recharts clsx tailwind-merge`
3.  **Create Base UI Components** (The building blocks)
    -   `Button`: Primary (blue), Ghost (sidebar links).
    -   `Input`: Clean borders with focus rings.
    -   `Card`: White background, subtle shadow, rounded corners.
    -   `Badge`: For status indicators (e.g., "Low Stock").

### Phase 2: Authentication Pages (Day 1-2)
**Goal**: Match the "Sign in" design exactly.

1.  **Login Page (`/login`)**
    -   Centered layout with gray background.
    -   White card container.
    -   Logo icon at top.
    -   Form fields: Username, Password (with eye icon toggle).
    -   "Forgot Password?" link.
    -   "Sign In" full-width blue button.
    -   "Sign Up" link at bottom.
2.  **Register Page (`/register`)**
    -   Similar layout to Login but with Name and Confirm Password fields.

### Phase 3: Application Layout (Day 2)
**Goal**: Build the "Shell" of the application (Sidebar + Header).

1.  **Sidebar Component**
    -   **Logo Area**: "ShopSync" with blue icon.
    -   **Navigation**: Dashboard, Inventory, Categories, Reports, Settings.
    -   **Active State**: Light blue background + blue text for current page.
    -   **User Profile**: Fixed at bottom with avatar and logout button.
2.  **Header Component**
    -   **Search Bar**: Large input with search icon.
    -   **Actions**: Notification bell, Theme toggle (Sun/Moon).
3.  **Main Layout Wrapper**
    -   Combine Sidebar + Header + Outlet (Page Content).
    -   Handle responsive mobile menu (hamburger).

### Phase 4: Dashboard Implementation (Day 3)
**Goal**: Build the data visualization dashboard.

1.  **Stats Cards**
    -   Create reusable `StatCard` component.
    -   Props: Title, Value, Trend (+20.1%), Icon.
    -   Implement the 4 cards: Revenue, Units Sold, Active Products, Out of Stock.
2.  **Sales Chart**
    -   Implement `SalesChart` using Recharts.
    -   Match the smooth curve (monotone) and blue gradient fill.
3.  **Recent Activity Feed**
    -   Create list component for right sidebar.
    -   Status icons (Green +, Red -, Yellow edit).
    -   Timestamp formatting ("15 minutes ago").

---

## 📝 Detailed Task List

### 1. Setup Tasks
- [ ] Run `npm install -D tailwindcss postcss autoprefixer`
- [ ] Run `npx tailwindcss init -p`
- [ ] Configure `index.css` with Tailwind directives.
- [ ] Install `lucide-react` for icons.

### 2. Component Development
- [ ] **`src/components/ui/Button.jsx`**
- [ ] **`src/components/ui/Input.jsx`**
- [ ] **`src/components/ui/Card.jsx`**
- [ ] **`src/components/layout/Sidebar.jsx`**
- [ ] **`src/components/layout/Header.jsx`**
- [ ] **`src/components/layout/Layout.jsx`**

### 3. Page Development
- [ ] **`src/pages/Login.jsx`** (Match design)
- [ ] **`src/pages/Dashboard.jsx`** (Match design)

---

## 🚀 Next Step

**Shall I start by installing Tailwind CSS and setting up the project structure to match these designs?**
