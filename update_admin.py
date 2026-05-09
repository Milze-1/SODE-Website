import re

with open('admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sidebar Link
sidebar_link_replacement = '''        <a href="#" onclick="showPage('media')" id="nav-media">
          <svg viewBox="0 0 24 24">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          Gallery & Videos
        </a>
        <a href="#" onclick="showPage('flyers')" id="nav-flyers">
          <svg viewBox="0 0 24 24">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
          Weekly Flyer
        </a>'''
content = content.replace('        <a href="#" onclick="showPage(\'media\')" id="nav-media">\n          <svg viewBox="0 0 24 24">\n            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />\n            <polyline points="17 8 12 3 7 8" />\n            <line x1="12" y1="3" x2="12" y2="15" />\n          </svg>\n          Gallery & Videos\n        </a>', sidebar_link_replacement)

# 2. Flyers Page HTML
flyers_page_html = '''      <!-- FLYERS -->
      <div class="page" id="page-flyers">
        <div class="page-header">
          <h1>Weekly Flyer</h1>
          <p>Manage the upcoming weekly session flyer displayed on the home page.</p>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="card-title">Flyers</div>
            <button class="btn btn-primary" onclick="openFlyerModal()">
              <svg viewBox="0 0 24 24">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg> Add Flyer
            </button>
          </div>
          <div id="flyerList"></div>
        </div>
      </div>

      <!-- CURRICULUM -->'''
content = content.replace('      <!-- CURRICULUM -->', flyers_page_html)

# 3. Flyers Modal HTML
flyers_modal_html = '''  <!-- FLYER MODAL -->
  <div class="modal-overlay" id="flyerModal">
    <div class="modal">
      <div class="modal-head">
        <h3 id="flyerModalTitle">Add Flyer</h3>
        <button class="modal-close" onclick="closeModal('flyerModal')">&times;</button>
      </div>
      <div class="modal-body">
        <input type="hidden" id="flyerEditIdx">
        <div class="form-row-2">
          <div class="form-group">
            <label>Week Label</label>
            <input type="text" id="flyerWeek" placeholder="e.g. This Week">
          </div>
          <div class="form-group">
            <label>Session Title</label>
            <input type="text" id="flyerTitle" placeholder="e.g. Module 1: Excellence">
          </div>
        </div>
        <div class="form-group">
          <label>Description (Optional)</label>
          <textarea id="flyerDesc" placeholder="Brief description of the session..." rows="3"></textarea>
        </div>
        <div class="form-row-2">
          <div class="form-group">
            <label>Time</label>
            <input type="text" id="flyerTime" placeholder="e.g. Every Sunday &middot; 8:00 AM">
          </div>
          <div class="form-group">
            <label>Location</label>
            <input type="text" id="flyerLocation" placeholder="e.g. Nigerian Law School, VI">
          </div>
        </div>
        <div class="form-group">
          <label>Flyer Image</label>
          <div style="display:flex;gap:10px;align-items:center;">
            <input type="text" id="flyerImage" placeholder="Image URL..." style="flex:1;">
            <label class="btn btn-ghost" style="margin:0;cursor:pointer;display:flex;align-items:center;padding:0 12px;font-size:12px;">
              Upload
              <input type="file" id="flyerImageFile" accept="image/*" style="display:none;" onchange="handleFlyerImageUpload(this)">
            </label>
          </div>
          <img id="flyerImagePreview" src="" style="max-height:100px;margin-top:10px;border-radius:6px;display:none;object-fit:cover;">
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-ghost" onclick="closeModal('flyerModal')">Cancel</button>
        <button class="btn btn-success" onclick="saveFlyerItem()">Save Flyer</button>
      </div>
    </div>
  </div>

  <!-- TOAST -->'''
content = content.replace('  <!-- TOAST -->', flyers_modal_html)

# 4. DEFAULT_FLYERS
content = content.replace('const DEFAULT_EVENTS = [', 'const DEFAULT_FLYERS = [];\n\n    const DEFAULT_EVENTS = [')

# 5. _cachedFlyers
content = content.replace('    let _cachedMedia = null;', '    let _cachedMedia = null;\n    let _cachedFlyers = null;')

# 6. getFlyers
content = content.replace('    function getMedia() { return _cachedMedia || DEFAULT_MEDIA; }', '    function getMedia() { return _cachedMedia || DEFAULT_MEDIA; }\n    function getFlyers() { return _cachedFlyers || DEFAULT_FLYERS; }')

# 7. saveFlyers
content = content.replace('    async function saveMedia(data) {\n      _cachedMedia = data;\n      try { await db.collection(\'sode_data\').doc(\'media\').set({ items: data }); } catch(e) { console.error(\'saveMedia:\', e); }\n    }', '    async function saveMedia(data) {\n      _cachedMedia = data;\n      try { await db.collection(\'sode_data\').doc(\'media\').set({ items: data }); } catch(e) { console.error(\'saveMedia:\', e); }\n    }\n    async function saveFlyers(data) {\n      _cachedFlyers = data;\n      try { await db.collection(\'sode_data\').doc(\'flyers\').set({ items: data }); } catch(e) { console.error(\'saveFlyers:\', e); }\n    }')

# 8. loadAllDataFromFirestore
content = content.replace("db.collection('sode_data').doc('media').get()", "db.collection('sode_data').doc('media').get(),\n          db.collection('sode_data').doc('flyers').get()")
content = content.replace("const [modSnap, spkSnap, evSnap, blgSnap, medSnap] = await Promise.all([", "const [modSnap, spkSnap, evSnap, blgSnap, medSnap, flyerSnap] = await Promise.all([")
content = content.replace("_cachedMedia = medSnap.exists ? medSnap.data().items : DEFAULT_MEDIA;", "_cachedMedia = medSnap.exists ? medSnap.data().items : DEFAULT_MEDIA;\n        _cachedFlyers = flyerSnap.exists ? flyerSnap.data().items : DEFAULT_FLYERS;")
content = content.replace("_cachedMedia = DEFAULT_MEDIA;\n      }", "_cachedMedia = DEFAULT_MEDIA;\n        _cachedFlyers = DEFAULT_FLYERS;\n      }")

# 9. render calls
content = content.replace("renderBlogs(); renderMediaAdmin(); renderSpeakers();", "renderBlogs(); renderMediaAdmin(); renderSpeakers(); renderFlyersAdmin();")

content = content.replace("if (name === 'speakers') renderSpeakers();", "if (name === 'speakers') renderSpeakers();\n      if (name === 'flyers') renderFlyersAdmin();")

content = content.replace("saveMedia(DEFAULT_MEDIA)\n      ]);", "saveMedia(DEFAULT_MEDIA),\n        saveFlyers(DEFAULT_FLYERS)\n      ]);")

content = content.replace("renderBlogs(); renderMediaAdmin();\n      toast('All data reset to defaults.');", "renderBlogs(); renderMediaAdmin(); renderFlyersAdmin();\n      toast('All data reset to defaults.');")


# 10. FLYER JS FUNCTIONS
flyer_js = '''
    // ─── FLYERS ───
    function renderFlyersAdmin() {
      const flyers = getFlyers();
      document.getElementById('flyerList').innerHTML = flyers.map((f, idx) => `
    <div class="event-admin-item">
      ${f.image ? `<img src="${f.image}" style="width:60px;height:60px;border-radius:6px;object-fit:cover;flex-shrink:0;">` : `<div style="width:60px;height:60px;border-radius:6px;background:var(--gray-200);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--gray-400);text-align:center;flex-shrink:0;">No Img</div>`}
      <div style="flex:1;">
        <div style="font-size:10px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--royal);margin-bottom:4px;">${f.week || 'This Week'}</div>
        <div class="event-admin-title">${f.title || 'Weekly Session'}</div>
      </div>
      <div class="module-actions">
        <button class="btn btn-ghost btn-sm" onclick="editFlyer(${idx})">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="deleteFlyer(${idx})">Delete</button>
      </div>
    </div>
  `).join('') || '<p style="color:var(--gray-400);font-size:14px;">No flyers added yet.</p>';
    }

    function openFlyerModal(f = null, idx = null) {
      document.getElementById('flyerModalTitle').textContent = f ? 'Edit Flyer' : 'Add Flyer';
      document.getElementById('flyerEditIdx').value = idx !== null ? idx : '';
      document.getElementById('flyerWeek').value = f ? (f.week || '') : '';
      document.getElementById('flyerTitle').value = f ? (f.title || '') : '';
      document.getElementById('flyerDesc').value = f ? (f.description || '') : '';
      document.getElementById('flyerTime').value = f ? (f.time || '') : '';
      document.getElementById('flyerLocation').value = f ? (f.location || '') : '';

      const imgUrl = f ? (f.image || '') : '';
      document.getElementById('flyerImage').value = imgUrl;
      const preview = document.getElementById('flyerImagePreview');
      if (imgUrl) { preview.src = imgUrl; preview.style.display = 'block'; }
      else { preview.src = ''; preview.style.display = 'none'; }
      document.getElementById('flyerImageFile').value = '';

      openModal('flyerModal');
    }

    function handleFlyerImageUpload(input) {
      const file = input.files[0];
      if (!file) return;
      openCropModal(file, async (dataUrl) => {
        const preview = document.getElementById('flyerImagePreview');
        preview.src = dataUrl;
        preview.style.display = 'block';
        input.value = '';
        try {
          toast('Uploading image...', 'success');
          const url = await uploadToStorage(dataUrl, 'flyers');
          document.getElementById('flyerImage').value = url;
          preview.src = url;
          toast('Image uploaded! ✓');
        } catch(e) {
          console.error('Upload failed:', e);
          document.getElementById('flyerImage').value = dataUrl;
          toast('Upload failed — image may not persist.', 'error');
        }
      });
    }

    function editFlyer(idx) {
      const flyers = getFlyers();
      if (flyers[idx]) openFlyerModal(flyers[idx], idx);
    }

    async function saveFlyerItem() {
      const idx = document.getElementById('flyerEditIdx').value;
      const f = {
        week: document.getElementById('flyerWeek').value.trim(),
        title: document.getElementById('flyerTitle').value.trim(),
        description: document.getElementById('flyerDesc').value.trim(),
        time: document.getElementById('flyerTime').value.trim(),
        location: document.getElementById('flyerLocation').value.trim(),
        image: document.getElementById('flyerImage').value.trim()
      };
      const flyers = getFlyers();
      if (idx !== '') flyers[idx] = f;
      else flyers.push(f);
      await saveFlyers(flyers);
      closeModal('flyerModal');
      renderFlyersAdmin(); renderDashboard(); toast(idx !== '' ? 'Flyer updated' : 'Flyer added');
    }

    async function deleteFlyer(idx) {
      if (!confirm('Are you sure you want to delete this flyer?')) return;
      const flyers = getFlyers(); flyers.splice(idx, 1);
      await saveFlyers(flyers); renderFlyersAdmin(); renderDashboard(); toast('Flyer deleted');
    }
'''
content = content.replace('    // ─── MODULES ───', flyer_js + '\n    // ─── MODULES ───')

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
