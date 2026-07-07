const GameAssets = {
    characters: {
        miner: {
            idle: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20idle%20pose%20yellow%20hard%20hat%20blue%20overalls%20holding%20pickaxe%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            mining: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20mining%20action%20swinging%20pickaxe%20yellow%20hard%20hat%20blue%20overalls%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            walk: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20walking%20pose%20yellow%20hard%20hat%20blue%20overalls%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            helmetLight: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20helmet%20with%20headlamp%20light%20on%20yellow%20hard%20hat%20front%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
        },
        miner2: {
            idle: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20idle%20pose%20orange%20hard%20hat%20green%20overalls%20holding%20shovel%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            mining: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20digging%20action%20orange%20hard%20hat%20green%20overalls%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd'
        },
        miner3: {
            idle: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20idle%20pose%20red%20hard%20hat%20brown%20overalls%20holding%20pickaxe%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            mining: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20miner%20character%20mining%20action%20red%20hard%20hat%20brown%20overalls%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd'
        },
        elevatorWorker: {
            idle: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20elevator%20operator%20worker%20idle%20orange%20hard%20hat%20blue%20uniform%20standing%20front%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            working: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20elevator%20operator%20worker%20pushing%20buttons%20orange%20hard%20hat%20blue%20uniform%20front%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd'
        },
        groundWorker: {
            idle: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20ground%20worker%20idle%20green%20shirt%20yellow%20hard%20hat%20standing%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            pushing: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20ground%20worker%20pushing%20mine%20cart%20green%20shirt%20yellow%20hard%20hat%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd'
        },
        supervisor: {
            miner: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20mining%20supervisor%20manager%20with%20clipboard%20suit%20and%20hard%20hat%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            elevator: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20elevator%20supervisor%20manager%20with%20clipboard%20suit%20and%20hard%20hat%20front%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd',
            ground: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20cute%20ground%20supervisor%20manager%20with%20clipboard%20business%20suit%20side%20view%20chibi%20style%20transparent%20background%20game%20sprite&image_size=square_hd'
        }
    },
    props: {
        elevator: {
            closed: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mine%20elevator%20cage%20with%20closed%20doors%20metal%20frame%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            open: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mine%20elevator%20cage%20with%20open%20doors%20metal%20frame%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
        },
        mineCart: {
            empty: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20empty%20mine%20cart%20red%20metal%20with%20wheels%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            full: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mine%20cart%20full%20of%20gold%20ore%20red%20metal%20with%20wheels%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
        },
        ores: {
            gold: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gold%20ore%20chunk%20shiny%20yellow%20rock%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            silver: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20silver%20ore%20chunk%20shiny%20gray%20rock%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            copper: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20copper%20ore%20chunk%20orange%20brown%20rock%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            diamond: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20diamond%20gem%20blue%20crystal%20shiny%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            ruby: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20ruby%20gem%20red%20crystal%20shiny%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
        },
        pickaxe: {
            wood: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20wooden%20pickaxe%20with%20stone%20head%20mining%20tool%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            iron: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20iron%20pickaxe%20mining%20tool%20wooden%20handle%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd',
            gold: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20golden%20pickaxe%20mining%20tool%20shiny%20wooden%20handle%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
        },
        conveyor: {
            belt: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20conveyor%20belt%20machine%20with%20rollers%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=landscape_4_3'
        }
    },
    scenes: {
        sky: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20blue%20sky%20with%20white%20clouds%20cute%20style%20game%20background%20tileable&image_size=landscape_16_9',
        mountains: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20green%20mountains%20with%20snow%20peaks%20cute%20style%20game%20background%20transparent%20background&image_size=landscape_16_9',
        groundTop: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20grass%20ground%20top%20layer%20with%20dirt%20below%20side%20view%20chibi%20style%20game%20tile%20asset&image_size=landscape_16_9',
        dirtLayer: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20brown%20dirt%20soil%20layer%20underground%20side%20view%20chibi%20style%20game%20tile%20asset&image_size=landscape_16_9',
        rockLayer: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gray%20rock%20stone%20layer%20underground%20mine%20wall%20side%20view%20chibi%20style%20game%20tile%20asset&image_size=landscape_16_9',
        mineTunnel: {
            wood: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mine%20tunnel%20with%20wooden%20support%20beams%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=landscape_16_9',
            stone: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mine%20tunnel%20with%20stone%20support%20pillars%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=landscape_16_9'
        },
        elevatorShaft: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20vertical%20mine%20elevator%20shaft%20with%20metal%20rails%20and%20ladder%20side%20view%20chibi%20style%20game%20background%20vertical&image_size=portrait_16_9',
        tower: {
            blue: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20blue%20mining%20tower%20building%20with%20red%20roof%20and%20window%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=portrait_4_3',
            green: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20green%20mining%20tower%20building%20with%20red%20roof%20and%20window%20side%20view%20chibi%20style%20transparent%20background%20game%20asset&image_size=portrait_4_3'
        },
        lamp: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20hanging%20mine%20lamp%20with%20warm%20yellow%20light%20glow%20chibi%20style%20transparent%20background%20game%20asset&image_size=square_hd'
    },
    ui: {
        buttons: {
            primary: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20golden%20rectangle%20button%20with%20rounded%20corners%20game%20UI%20element%20transparent%20background&image_size=square_hd',
            green: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20green%20rectangle%20button%20with%20rounded%20corners%20game%20UI%20element%20transparent%20background&image_size=square_hd',
            blue: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20blue%20rectangle%20button%20with%20rounded%20corners%20game%20UI%20element%20transparent%20background&image_size=square_hd',
            red: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20red%20rectangle%20button%20with%20rounded%20corners%20game%20UI%20element%20transparent%20background&image_size=square_hd'
        },
        icons: {
            gold: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gold%20coin%20icon%20with%20dollar%20sign%20shiny%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            gem: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20blue%20diamond%20gem%20icon%20shiny%20crystal%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            cash: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20green%20cash%20money%20bill%20icon%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            settings: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gear%20settings%20icon%20gray%20metal%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            music: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20music%20note%20icon%20colorful%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            pickaxe: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20pickaxe%20icon%20mining%20tool%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            elevator: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20elevator%20icon%20lift%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            factory: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20factory%20building%20icon%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            mountain: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mountain%20peak%20icon%20with%20snow%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd'
        },
        panels: {
            topBar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20dark%20game%20top%20bar%20panel%20with%20gold%20border%20UI%20element%20transparent%20background&image_size=landscape_16_9',
            bottomNav: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20dark%20game%20bottom%20navigation%20bar%20panel%20with%20gold%20border%20top%20UI%20element%20transparent%20background&image_size=landscape_16_9',
            modal: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20game%20modal%20popup%20panel%20with%20golden%20border%20dark%20background%20UI%20element%20transparent%20background&image_size=square_hd',
            card: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20game%20upgrade%20card%20panel%20dark%20with%20golden%20border%20UI%20element%20transparent%20background&image_size=landscape_4_3'
        },
        badges: {
            level: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20golden%20circular%20level%20badge%20with%20number%20space%20chibi%20style%20transparent%20background%20game%20UI%20element&image_size=square_hd',
            lock: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20padlock%20lock%20icon%20metal%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd',
            check: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20green%20checkmark%20badge%20chibi%20style%20transparent%20background%20game%20UI%20icon&image_size=square_hd'
        }
    },
    effects: {
        mining: {
            frame1: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mining%20spark%20effect%20frame%201%20small%20stars%20and%20dust%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
            frame2: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mining%20spark%20effect%20frame%202%20medium%20stars%20and%20dust%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
            frame3: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20mining%20spark%20effect%20frame%203%20large%20burst%20stars%20and%20dust%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd'
        },
        goldCollect: {
            frame1: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gold%20coin%20collect%20effect%20frame%201%20coin%20flying%20up%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
            frame2: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20gold%20coin%20collect%20effect%20frame%202%20coin%20sparkle%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd'
        },
        levelUp: {
            frame1: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20level%20up%20effect%20frame%201%20light%20rays%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
            frame2: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20level%20up%20effect%20frame%202%20star%20burst%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
            frame3: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20level%20up%20effect%20frame%203%20confetti%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd'
        },
        dust: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20dust%20cloud%20effect%20brown%20particles%20chibi%20style%20transparent%20background%20game%20effect&image_size=square_hd',
        lightGlow: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=2D%20cartoon%20warm%20yellow%20light%20glow%20effect%20radial%20gradient%20transparent%20background%20game%20effect&image_size=square_hd'
    }
};