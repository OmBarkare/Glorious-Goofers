import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Github, Download } from "lucide-react"

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <span className="font-bold">Streamline Extension</span>
        </Link>
        <nav className="flex flex-1 items-center space-x-6 text-sm font-medium">
          <Link href="#installation" className="transition-colors hover:text-primary">
            Installation
          </Link>
          <Link href="#features" className="transition-colors hover:text-primary">
            Features
          </Link>
          <Link href="#support" className="transition-colors hover:text-primary">
            Support
          </Link>
        </nav>
        <div className="flex items-center space-x-4">
          <Link href="https://github.com/Meet-Patel03/Glorious-Goofers" target="_blank" rel="noreferrer">
            <Button variant="ghost" size="icon">
              <Github className="h-4 w-4" />
              <span className="sr-only">GitHub</span>
            </Button>
          </Link>
          <Button variant="ghost" size="sm">
            Help
          </Button>
          <Button size="sm">
            <Download className="mr-2 h-4 w-4" />
            Download
          </Button>
        </div>
      </div>
    </header>
  )
}
