import { NavLink } from "react-router"
import "./style.css"

export interface TabBarProps extends
  React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> {
  tabs: {
    label: string
    path: string
  }[]
}

const TabBar: React.FC<TabBarProps> = ({ tabs, ...props }) => {
  return (
    <nav {...props}>
      {tabs.map(tab => (
        <NavLink to={tab.path} key={tab.path}>
          {tab.label}
        </NavLink>
      ))}
    </nav>
  )
}

export default TabBar
