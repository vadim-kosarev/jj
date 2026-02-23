package home.art.tst;

import lombok.extern.slf4j.Slf4j;

import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

@Slf4j
public class CFSample implements AutoCloseable {

    //    ExecutorService ex = Executors.newVirtualThreadPerTaskExecutor();
    ExecutorService ex = Executors.newFixedThreadPool(2);
    private static final Random random = new Random();

    private String calcSource() {

        log.info("calculating source... in `{}`", Thread.currentThread().getName());
        try {
            TimeUnit.MILLISECONDS.sleep(random.nextInt(1000, 2500));
            log.info("Calculated");
            return "This is a source line (this is a single line)";
        } catch (InterruptedException e) {
            log.error("Exception in calcSource", e);
            throw new RuntimeException(e);
        }

    }

    public void simpleCF() {
        log.info("simpleCF started...");
        var cf = CompletableFuture.supplyAsync(this::calcSource, ex)
                .thenApply(String::toUpperCase)
                .thenAccept(log::info);

        var cf2 = CompletableFuture.supplyAsync(this::calcSource, ex)
                .thenApply(s -> s.replace("line", "__LINE__"))
                .thenAccept(log::info);

        log.info("simpleCF before join...: {}", cf);
        CompletableFuture.allOf(cf, cf2).join();

        log.info("simpleCF ended...: {}", cf);
    }

    @Override
    public void close() throws Exception {
        log.info("Close...");

        ex.shutdown();

        if (!ex.awaitTermination(5, TimeUnit.SECONDS)) {
            ex.shutdownNow();
        }

        log.info("Close...DONE");
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Hello from CFSample!");
        TimeUnit.SECONDS.sleep(1);

        try (CFSample cf = new CFSample()) {
            cf.simpleCF();
            log.info("Exit main....");
        } catch (Throwable th) {
            log.error("Error in main", th);
        }
    }

}
