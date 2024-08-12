import botAvatar from '../assets/sara_avatar.jpg'
import userAvatar from '../assets/userAvatar.png'
//import {defaultQuickReplies} from "./quickReplys";
import {createTextBotMsg} from "../utils/msgManager";


const initialMessages = [
	createTextBotMsg('喵喵客服进入对话，为你服务！', 'system'),
	createTextBotMsg('小主您好！喵喵客服为您服务，请提供您想咨询的订单号，喵喵将以最快速度为您提供满意回复~'),
];

function initNavBar() {
	return {
		title: '喵喵客服'
	}
}

export function initBotConfig() {
	return {
		avatar: botAvatar
	}
}

function initUserConfig() {
	return {
		avatar: userAvatar
	}
}


export const BotConfig = {
	navbar: initNavBar(),
	robot: initBotConfig(),
	user: initUserConfig(), 	// 用户头像
	messages: initialMessages,
	placeholder: '随便输点...', // 输入框占位符
	toolbar: [
		{
			type: 'image',
			icon: 'image',
			title: '相册',
		},
	],
}
