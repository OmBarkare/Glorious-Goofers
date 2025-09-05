import { Button } from "@/components/ui/button"
import { Download, HelpCircle } from "lucide-react"

export default function CTA() {
  return (
    <section className="border-t">
      <div className="container flex flex-col items-center gap-4 py-24 text-center md:py-32">
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">
          Ready to enhance your browsing experience?
        </h2>
        <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
          Download our Chrome extension now and start tracking your activities with powerful insights and productivity
          tools.
        </p>
        <div className="flex gap-4 mt-4">
          <Button size="lg">
            <Download className="mr-2 h-4 w-4" />
            Download Extension
          </Button>
          <Button variant="outline" size="lg">
            <HelpCircle className="mr-2 h-4 w-4" />
            Need Help?
          </Button>
        </div>
      </div>
    </section>
  )
}
