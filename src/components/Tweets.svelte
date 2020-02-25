<script>
  import { data, depute } from "./stores";
  import { trackAction } from "./tracking";
  const { tweets, mailto_qs: mailTo } = data;
  let offset = 0;
  let currentTweets;

  $: currentTweets = [
    tweets[offset % tweets.length],
    tweets[(offset + 1) % tweets.length]
  ];
</script>

<style>
  .autres {
    text-align: right;
  }

  .autres a {
  }
</style>

<h5 class="sl">Je lui envoie aussi un tweet</h5>
{#if $depute.twitter.length}
  <div class="autres">
    <a href="#" on:click|preventDefault={() => (offset += 2)}>
      je veux voir d'autres tweets !
    </a>
  </div>
  <div class="row pt-2">
    {#each currentTweets.slice() as { id, tweet, quoted }}
      <div class="col-6">
        <div class="reseau">{tweet}</div>
        <a
          on:click={() => trackAction('EnvoyerTweet', id)}
          href="https://twitter.com/intent/tweet?text={$depute.twitter}%20{quoted}&amp;hashtags=allod%C3%A9put%C3%A9"
          class="btn-cust b2 my-2"
          target="_blank">
          Envoyer ce tweet
        </a>
      </div>
    {/each}
  </div>
{:else}
  <div id="no-twitter" class="col align-self-center lead">
    Nous ne connaissons pas le compte twitter de
    <span class="depute_article_demonstratif">
      {$depute.article_demonstratif} {$depute.titre}
    </span>
    !
  </div>
{/if}
