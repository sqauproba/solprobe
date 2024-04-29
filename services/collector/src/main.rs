use solprobe_collector::run;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    run().await
}
