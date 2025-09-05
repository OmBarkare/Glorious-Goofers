import { Download, Settings, Chrome, CheckCircle } from "lucide-react"

const installationSteps = [
  {
    name: "Download Extension",
    description: "Click the download button above to get the latest version of our Chrome extension (.crx file).",
    icon: Download,
    step: "Step 1",
  },
  {
    name: "Enable Developer Mode",
    description: "Open Chrome Settings > Extensions, then toggle 'Developer mode' in the top-right corner.",
    icon: Settings,
    step: "Step 2",
  },
  {
    name: "Install Extension",
    description: "Drag and drop the downloaded .crx file into the Chrome Extensions page to install.",
    icon: Chrome,
    step: "Step 3",
  },
  {
    name: "Start Using",
    description: "Pin the extension to your toolbar and start enjoying enhanced productivity features.",
    icon: CheckCircle,
    step: "Step 4",
  },
]

export default function Features() {
  return (
    <section className="container space-y-16 py-24 md:py-32">
      <div className="mx-auto max-w-[58rem] text-center">
        <h2 className="font-bold text-3xl leading-[1.1] sm:text-3xl md:text-5xl">Installation Guide</h2>
        <p className="mt-4 text-muted-foreground sm:text-lg">
          Follow these simple steps to install and start using our Chrome extension.
        </p>
      </div>
      <div className="mx-auto grid max-w-5xl grid-cols-1 gap-8 md:grid-cols-2">
        {installationSteps.map((step) => (
          <div key={step.name} className="relative overflow-hidden rounded-lg border bg-background p-8">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <step.icon className="h-6 w-6 text-primary" />
              </div>
              <div>
                <div className="text-sm font-medium text-muted-foreground">{step.step}</div>
                <h3 className="font-bold">{step.name}</h3>
              </div>
            </div>
            <p className="mt-4 text-muted-foreground">{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
