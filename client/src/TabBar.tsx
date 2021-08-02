import { Link } from '@reach/router'

export interface TabBarProps {
  tabs: {
    label: string
    path: string
  }[]
}

const TabBar: React.FC<TabBarProps> = ({ tabs }) => {
  return (
    <nav>
      {tabs.map((tab, index) => (
        <Link
          style={{
            padding: 16,
            paddingTop: 4,
            paddingBottom: 5,
            color: 'white',
            textDecoration: 'none',
            backgroundColor: '#333',
            borderRadius: '0.25rem',
            marginRight: index !== 0 ? 0 : 8,
          }}
          to={tab.path}
        >
          {tab.label}
        </Link>
      ))}
    </nav>
  )
}

export default TabBar
