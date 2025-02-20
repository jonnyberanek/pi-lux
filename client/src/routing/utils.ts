import { useResolvedPath, useLocation, matchRoutes, RouteObject } from "react-router"
import { useMemo } from "react"

export function useResolvedRoute(routes: RouteObject[], rpath: string = ".") {
  const path = useResolvedPath(rpath)
  const location = useLocation()

  return useMemo(() => {
    const match = matchRoutes(routes, location)?.find(m => m.pathname === path.pathname)
    if (!match) {
      throw Error("Route not found")
    }
    return match
  }, [path, location, routes])
}