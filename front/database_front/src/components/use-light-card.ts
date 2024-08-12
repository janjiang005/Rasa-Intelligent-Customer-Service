import { onMounted, onUnmounted, ref } from 'vue';

interface IOptions {
    light?: {
        width?: number;
        height?: number;
        color?: string;
        blur?: number;
    };
}

export const useLightCard = (option: IOptions = {}) => {
    // 获取卡片的dom节点
    const cardRef = ref<HTMLDivElement | null>(null);
    let cardOverflow = '';
    // 光的dom节点
    const lightRef = ref<HTMLDivElement>(document.createElement('div'));

    // 设置光源的样式
    const setLightStyle = () => {
        const { width = 80, height = 80, color = '#ff4132', blur = 40 } = option.light ?? {};
        const lightDom = lightRef.value;
        lightDom.style.position = 'absolute';
        lightDom.style.width = `${width}px`;
        lightDom.style.height = `${height}px`;
        lightDom.style.background = color;
        lightDom.style.filter = `blur(${blur}px)`;
    };

    // 设置卡片的overflow为hidden
    const setCardOverflowHidden = () => {
        const cardDom = cardRef.value;
        if (cardDom) {
            cardOverflow = cardDom.style.overflow;
            cardDom.style.overflow = 'hidden';
        }
    };

    // 还原卡片的overflow
    const restoreCardOverflow = () => {
        const cardDom = cardRef.value;
        if (cardDom) {
            cardDom.style.overflow = cardOverflow;
        }
    };

    // 往卡片添加光源
    const addLight = () => {
        const cardDom = cardRef.value;
        if (cardDom) {
            cardDom.appendChild(lightRef.value);
        }
    };

    // 删除光源
    const removeLight = () => {
        const cardDom = cardRef.value;
        if (cardDom) {
            cardDom.removeChild(lightRef.value);
        }
    };

    // 监听卡片的鼠标移入
    const onMouseEnter = () => {
        addLight();
        setCardOverflowHidden();
    };

    // 监听卡片的鼠标移动
    const onMouseMove = (e: MouseEvent) => {
        const { clientX, clientY } = e;
        const cardDom = cardRef.value;
        const lightDom = lightRef.value;
        if (cardDom) {
            const { x, y } = cardDom.getBoundingClientRect();
            const { width, height } = lightDom.getBoundingClientRect();
            lightDom.style.left = `${clientX - x - width / 2}px`;
            lightDom.style.top = `${clientY - y - height / 2}px`;

            const maxXRotation = 10; // X轴旋转角度
            const maxYRotation = 10; // Y轴旋转角度
            const rangeX = 200 / 2; // X轴旋转的范围
            const rangeY = 200 / 2; // Y轴旋转的范围

            const rotateX = ((clientY - y - rangeY) / rangeY) * maxXRotation;
            const rotateY = ((clientX - x - rangeX) / rangeX) * maxYRotation;

            cardDom.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        }
    };

    // 监听卡片鼠标移出
    const onMouseLeave = () => {
        removeLight();
        restoreCardOverflow();
    };

    onMounted(() => {
        setLightStyle();
        cardRef.value?.addEventListener('mouseenter', onMouseEnter);
        cardRef.value?.addEventListener('mousemove', onMouseMove);
        cardRef.value?.addEventListener('mouseleave', onMouseLeave);
    });

    onUnmounted(() => {
        cardRef.value?.removeEventListener('mouseenter', onMouseEnter);
        cardRef.value?.removeEventListener('mousemove', onMouseMove);
        cardRef.value?.removeEventListener('mouseleave', onMouseLeave);
    });

    return {
        cardRef,
    };
};
