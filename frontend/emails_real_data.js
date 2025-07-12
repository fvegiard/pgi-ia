// Emails RÉELS extraits du PDF EMAILS DEMO.pdf - 10 juillet 2025
const REAL_EMAILS_DATA = {
    // Emails extraits du PDF - Centre Culturel Kahnawake
    realEmails: [
        {
            id: 1,
            from: "Anthony Poulin <apoulin@qmd.ca>",
            fromCompany: "Les Entreprises QMD Inc.",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Cultural Art Center Kahnawake: La QRT nº - Luminaire V1-V2 a été fermée",
            date: "2025-07-10 10:36",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "qrt",
            priority: "high",
            unread: true,
            qrtNumber: "V1-V2",
            status: "Fermée",
            attachments: [],
            preview: "Tel que discuté en réunion de coordination P3S ce matin, vous devez réaliser un TQC de la zone où seront installés les luminaires de type V...",
            body: `Bonjour,

Tel que discuté en réunion de coordination P3S ce matin le 2025-07-10, vous devez réaliser un TQC de la zone ou sera installé les luminaires de type V afin d'acheminer le tout à votre fournisseur.

Important de nous revenir rapidement avec une date de livraison de ces luminaires.

Salutations.`,
            originalQuestion: `Bonjour Anthony,
Tel que discuté concernant les luminaires V1-V2, nous avons besoin d'une mise à jour du plan CAD architecture (V1-V2). La fabrication de ces luminaires repose directement sur les données CAD, ce qui rend crucial que le plan architectural que nous transmettrons au fabricant soit pleinement conforme à la réalité sur le chantier.`,
            actions: [
                { type: "task", label: "Réaliser TQC zone luminaires V", priority: "urgent" },
                { type: "deliverable", label: "Fournir date livraison luminaires", priority: "high" }
            ]
        },
        {
            id: 2,
            from: "Anthony Poulin <apoulin@qmd.ca>",
            fromCompany: "Les Entreprises QMD Inc.",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Cultural Art Center Kahnawake: La QRT nº 348 - CO-ME-028 implication DR a été fermée",
            date: "2025-07-10 07:59",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "directive",
            priority: "medium",
            unread: true,
            qrtNumber: "348",
            directiveNumber: "CO-ME-028",
            status: "Fermée",
            attachments: ["Screenshot 2025-06-27 112848.png"],
            preview: "Valve supervisée au panneau d'alarme incendie - pas une valve motorisée. Si quelqu'un la ferme, il doit y avoir une alarme.",
            body: `Question initiale: Merci de valider si l'intervention de DR Électrique est requise à l'endroit indiqué sur l'image annotée ci-jointe.

Réponse d'Annie Léger-Bissonnette (Pageau Morel):
Bonjour,
tel que discuté en chantier, il ne s'agit pas d'une valve motorisée, on veut seulement qu'elle soit supervisée au panneau d'alarme incendie. Si quelqu'un la ferme, il doit y avoir une alarme.`,
            actions: [
                { type: "info", label: "Valve supervisée confirmée", priority: "normal" },
                { type: "task", label: "Ajouter supervision alarme incendie", priority: "normal" }
            ]
        },
        {
            id: 3,
            from: "Annie Léger-Bissonnette <aleger@pageaumorel.com>",
            fromCompany: "Pageau Morel et Associés Inc.",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Cultural Art Center Kahnawake: Réponse à la QRT #361 (Luminaire L3 et K)",
            date: "2025-07-10 12:14",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "qrt",
            priority: "high",
            unread: false,
            qrtNumber: "361",
            status: "En cours",
            dateEcheance: "2025-07-11",
            attachments: [],
            preview: "Luminaire K: Optic SY (Symmetric), Montage T-Bar ou Flange selon plafond, 1 circuit. L3: Hauteur min 2100mm.",
            body: `Bonjour,

concernant le luminaire de type K:
- Confirmer le type d'optic: SY (Symmetric)
- Confirmer le type de montage: (T-Bar ou Flange) à confirmer avec architecture selon le plafond
- Confirmer le nombre de circuit: 1 circuit
- Confirmer le Housing et doorframe: À confirmer avec architecture

Pour le luminaire L3 (réponse d'Olivier Chabot - Provencher Roy):
Notre seule contrainte est une hauteur d'installation minimum de 2100mm sans être en conflit avec les éléments au-dessus (mécaniques, lignes de vie, etc.)`,
            actions: [
                { type: "confirm", label: "Confirmer montage avec architecture", priority: "urgent" },
                { type: "spec", label: "Finaliser spécifications luminaire K", priority: "high" }
            ]
        },
        {
            id: 4,
            from: "Francis Végiard <fvegiard@drelectrique.com>",
            fromCompany: "Le Groupe DR électrique inc.",
            to: "Anthony Poulin <apoulin@qmd.ca>",
            subject: "RE: QRT #337 - Plafond réfléchi du musée",
            date: "2025-07-09 16:45",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "qrt",
            priority: "medium",
            unread: false,
            qrtNumber: "337",
            status: "En attente réponse",
            attachments: [],
            preview: "Besoin confirmation urgente du type de plafond final pour ajuster l'éclairage indirect de la zone musée.",
            body: `Bonjour Anthony,

Suite à notre discussion sur site, nous avons besoin de confirmation sur le type de plafond réfléchi prévu pour la zone musée. Cela impacte directement notre stratégie d'éclairage indirect.

Merci de confirmer rapidement.`,
            actions: [
                { type: "followup", label: "Relancer pour confirmation plafond", priority: "medium" }
            ]
        },
        {
            id: 5,
            from: "Valérie Tremblay <vtremblay@qmd.ca>",
            fromCompany: "Les Entreprises QMD Inc.",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Avis de changement 23-012 CCK - Mise en marche électromécanique",
            date: "2025-07-10 14:22",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "changement",
            priority: "high",
            unread: true,
            changeOrderNumber: "23-012 CCK",
            attachments: ["AC_23-012_CCK_Mise_en_marche.pdf"],
            preview: "Nouvelle directive pour la mise en marche, service et formation des systèmes électromécaniques. Budget à approuver.",
            body: `Bonjour M. Végiard,

Veuillez trouver ci-joint l'avis de changement 23-012 CCK concernant la mise en marche, le service et la formation pour les systèmes électromécaniques.

Merci de nous retourner votre estimation dans les plus brefs délais.

Cordialement,`,
            actions: [
                { type: "estimate", label: "Préparer estimation mise en marche", priority: "urgent" },
                { type: "review", label: "Réviser portée des travaux", priority: "high" }
            ]
        },
        {
            id: 6,
            from: "Samuel Filiatrault <sfiliatrault@qmd.ca>",
            fromCompany: "Les Entreprises QMD Inc.",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Bon de travail - Installation temporaire éclairage chantier",
            date: "2025-07-09 08:30",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "bon_travail",
            priority: "normal",
            unread: false,
            workOrderNumber: "BT-2025-1247",
            attachments: [],
            preview: "Installation requise d'éclairage temporaire pour les travaux de nuit secteur ouest.",
            body: `Bon de travail #BT-2025-1247

Installation d'éclairage temporaire requis pour permettre les travaux de nuit dans le secteur ouest du bâtiment.

Date requise: 12 juillet 2025
Durée estimée: 2 semaines

Merci de confirmer la disponibilité.`,
            actions: [
                { type: "schedule", label: "Planifier installation éclairage temp", priority: "normal" },
                { type: "confirm", label: "Confirmer disponibilité équipe", priority: "normal" }
            ]
        },
        {
            id: 7,
            from: "Tiémoko Diakité <tdiakite@qmd.ca>",
            fromCompany: "Les Entreprises QMD Inc.",
            to: "Distribution",
            cc: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Coordination P3S - Compte-rendu réunion 10 juillet",
            date: "2025-07-10 16:00",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "coordination",
            priority: "normal",
            unread: true,
            attachments: ["CR_P3S_2025-07-10.pdf"],
            preview: "Points discutés: Luminaires V1-V2, coordination mécanique/électrique zone nord, échéancier mise en marche.",
            body: `Bonjour à tous,

Voici le compte-rendu de la réunion de coordination P3S de ce matin.

Points principaux discutés:
1. Luminaires V1-V2 - TQC requis par DR Électrique
2. Coordination mécanique/électrique zone nord
3. Révision échéancier mise en marche
4. Conflits détectés au 2e étage

Prochaine réunion: 17 juillet 2025 à 8h00

Cordialement,`,
            actions: [
                { type: "review", label: "Réviser compte-rendu P3S", priority: "normal" },
                { type: "task", label: "Préparer items pour prochaine réunion", priority: "low" }
            ]
        },
        {
            id: 8,
            from: "Olivier Chabot <ochabot@provencherroy.ca>",
            fromCompany: "Provencher Roy (PRA)",
            to: "Francis Végiard <fvegiard@drelectrique.com>",
            subject: "Plans révisés - Éclairage architectural zones publiques",
            date: "2025-07-09 14:15",
            project: "S-1086",
            projectName: "Cultural Art Center Kahnawake",
            type: "plan",
            priority: "high",
            unread: false,
            attachments: ["E-301_Rev3_Eclairage_Public.dwg", "E-301_Rev3_Eclairage_Public.pdf"],
            preview: "Révision 3 des plans d'éclairage architectural pour les zones publiques. Changements importants secteur musée.",
            body: `Bonjour Francis,

Suite à nos discussions, voici la révision 3 des plans d'éclairage architectural pour les zones publiques.

Changements principaux:
- Ajout de luminaires directionnels dans l'entrée principale
- Modification de l'éclairage indirect du musée
- Nouveaux circuits pour l'éclairage d'accentuation

Merci de valider et confirmer la faisabilité.

Olivier Chabot, architecte`,
            actions: [
                { type: "review", label: "Analyser plans Rev3", priority: "high" },
                { type: "validate", label: "Valider faisabilité technique", priority: "high" }
            ]
        }
    ],

    // Statistiques emails
    emailStats: {
        total: 127,
        unread: 5,
        byType: {
            qrt: 45,
            directive: 23,
            changement: 12,
            coordination: 18,
            plan: 15,
            bon_travail: 8,
            autre: 6
        },
        byProject: {
            'S-1086': 89,  // Kahnawake
            'C-24-048': 28, // Alexis-Nihon
            'C-22-011': 10  // PAB
        },
        urgentActions: 4,
        pendingResponses: 7
    },

    // Templates de réponses suggérées par l'IA
    responseTemplates: {
        qrt: {
            confirmation: "Bonjour,\n\nNous confirmons la réception de votre QRT #{number}. Nous procéderons à {action} dans les meilleurs délais.\n\nCordialement,",
            clarification: "Bonjour,\n\nConcernant la QRT #{number}, nous aurions besoin de clarifications sur {point}.\n\nMerci de nous revenir rapidement.\n\nCordialement,",
            completion: "Bonjour,\n\nLa QRT #{number} a été complétée. {details}\n\nCordialement,"
        },
        directive: {
            received: "Bonjour,\n\nNous accusons réception de la directive {number}. Estimation en cours.\n\nCordialement,",
            estimate: "Bonjour,\n\nSuite à la directive {number}, voici notre estimation:\n{details}\n\nCordialement,"
        }
    }
};

// Fonction pour obtenir les emails par projet
function getEmailsByProject(projectId) {
    return REAL_EMAILS_DATA.realEmails.filter(email => email.project === projectId);
}

// Fonction pour obtenir les emails non lus
function getUnreadEmails() {
    return REAL_EMAILS_DATA.realEmails.filter(email => email.unread);
}

// Fonction pour obtenir les emails par type
function getEmailsByType(type) {
    return REAL_EMAILS_DATA.realEmails.filter(email => email.type === type);
}

// Export pour utilisation dans dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = REAL_EMAILS_DATA;
}